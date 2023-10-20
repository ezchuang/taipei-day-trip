from flask import ( Blueprint, request, jsonify, redirect)
from datetime import datetime
import requests
from dotenv import load_dotenv
import os

from modal import token
from modal.modal_folder import modal_orders


blueprint_orders = Blueprint('blueprint_orders', __name__, url_prefix ="/api")

dotenv_path = 'partner_key.env'
load_dotenv(dotenv_path)
partner_key = os.getenv("PARTNER_KEY")


# 取得所有已下訂行程
@blueprint_orders.route("/orders", methods=["GET"])
@token.token_required
def orders_get_all(user_info, http_code):
    res = {}

    # 驗證失敗
    if "error" in user_info:
        if http_code == 403:
            res = user_info
            return redirect("/")
        return jsonify(res), http_code

    # 取得所有 order info
    try:
        data = modal_orders.orders_get_all(user_info["id"])

        res = {
            "data": data,
        }
        http_code = 200
        return jsonify(res), http_code
    
    except Exception as err:
        print(err)
        res = {
            "data": None,
        }
        http_code = 200
        return jsonify(res), http_code


# 下訂行程
@blueprint_orders.route("/orders", methods=["POST"])
@token.token_required
def orders_post(user_info, http_code):
    res = {}

    # 驗證失敗
    if "error" in user_info:
        if http_code == 403:
            res = user_info
            return redirect("/")
        return jsonify(res), http_code

    # 建立訂單 & 付款
    input_data = request.get_json()

    try:
        total_price = input_data["order"]["price"]
        trip = input_data["order"]["trip"]

        # 檢查輸入資訊
        db_data = modal_orders.booking_get_for_order(user_info["id"])

        for i in range(len(db_data)):
            total_price -= db_data[i]["price"]
            if total_price < 0:
                raise ValueError
            if not db_data[i]["booking_id"] == trip[i]["attraction"]["bookingId"] or \
                not db_data[i]["id"] == trip[i]["attraction"]["id"] or \
                not db_data[i]["date"] == trip[i]["date"] or \
                not db_data[i]["time"] == trip[i]["time"]:
                raise ValueError

        # 生成 order id
        date_today = datetime.now()
        date_today_str = datetime.strftime(date_today, "%Y%m%d%H%M%S")
        order_id = date_today_str
        # if not current_app.config.get("date_today") or current_app.config["date_today"] < date_today:
        #     current_app.config["date_today"] = date_today
        #     current_app.config["order_sequence"] = 0
        # current_app.config["order_sequence"] += 1
        # 下列等同於 date_today_str + str(current_app.config["order_sequence"]).zfill(6)
        # order_id = date_today_str + ("%06d" % current_app.config["order_sequence"])

        # 寫入 orders
        sql_res = modal_orders.orders_post_orders(order_id, user_info["id"], input_data)

        if not sql_res:
            raise ValueError("failed to create order")
        
        # 寫入 orders detail
        for db_data_sep in db_data:
            sql_res = modal_orders.orders_post_orders_detail(order_id, db_data_sep)

            if not sql_res:
                raise ValueError("failed to create order")
        
        # fetch tap pay api
        url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
        body = {
            "prime": input_data["prime"],
            "partner_key": partner_key,
            "merchant_id": "Ezpay99_CTBC",
            "details": "TapPay Test",
            "amount": input_data["order"]["price"],
            "cardholder": {
                "phone_number": f'+886{input_data["order"]["contact"]["phone"][1:]}',
                "name": input_data["order"]["contact"]["name"],
                "email": input_data["order"]["contact"]["email"],
            },
        }
        headers = {
            "Content-Type": "application/json",
            "x-api-key": partner_key
        }
        response = requests.post(url, headers=headers, json=body)
        response = response.json()
        if response["status"] != 0:
            msg = response["msg"]
            raise ValueError("訂單建立失敗")

        # 刪除暫存之預定資料
        db_data = modal_orders.orders_set_delete_booking(user_info["id"])

        # 更新訂單狀態
        db_data = modal_orders.orders_set_update_orders(order_id)

        res = {
            "data" : {
                "number": order_id,
                "payment": {
                    "status": 0,
                    "message": "付款成功"
                }
            }
        }
        return jsonify(res), 200
    
    
    except ValueError as err:
        print("ERROR: ", err)
        msg = "訂單建立失敗，輸入不正確或其他原因"
        res = {
            "error": True,
            "message": msg,
        }
        return jsonify(res), 400


# 查詢行程
@blueprint_orders.route("/orders/<int:order_id>", methods=["GET"])
@token.token_required_special
def orders_get(user_info, http_code, order_id=None):
    res = {}

    # 驗證失敗
    if "error" in user_info:
        if http_code == 403:
            res = user_info
            return redirect("/")
        return jsonify(res), http_code

    # 依據 order id 取得 order info
    try:
        data = modal_orders.orders_get(user_info["id"], order_id)

        # 上面挑戰減少 access DB 次數，下面要重新組裝
        price = data[0]["price"]
        name = data[0]["name"]
        email = data[0]["email"]
        phone = data[0]["phone"]
        status = data[0]["status"]
        for index in range(len(data)):
            data[index] = {
                "attraction": {
                    "id": data[index]["id"],
                    "name": data[index]["attraction_name"],
                    "address": data[index]["address"],
                    "image": data[index]["images"].split(",")[0]
                },
                "date": data[index]["date"],
                "time": data[index]["time"],
            }

        res = {
            "data": {
                "number": order_id,
                "price": price,
                "trip": data,
                "contact": {
                    "name": name,
                    "email": email,
                    "phone": phone,
                },
                "status": status
            }  
        }
        http_code = 200
        return jsonify(res), http_code
    
    except Exception as err:
        print(err)
        res = {
            "data": None,
        }
        http_code = 200
        return jsonify(res), http_code