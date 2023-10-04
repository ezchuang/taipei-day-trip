from flask import ( Blueprint, request, jsonify, redirect)
# from functools import wraps
# from datetime import datetime, timedelta

from module import token
from .api_user import secret_key
import module.flask_modules as flask_modules
from controller import qry_para_set


blueprint_booking = Blueprint('blueprint_booking', __name__, url_prefix ="/api")


# 預定行程
@blueprint_booking.route("/booking", methods=["GET", "POST", "DELETE"])
@token.token_required
def booking(user_info, http_code):
    res = {}

    # 驗證失敗
    if "error" in user_info:
        if http_code == 403:
            res = user_info
            return redirect("/")
        return jsonify(res), http_code

    # 取得尚未下單的預定行程
    if request.method == "GET":
        try:
            command_paras = qry_para_set.booking_get(user_info["id"])
            data = flask_modules.query_fetch_all(command_paras)
            # 上面挑戰減少 access DB 次數，下面要重新組裝
            for index in range(len(data)):
                data[index] = {
                    "attraction": {
                        "bookingId": data[index]["booking_id"],
                        "id": data[index]["id"],
                        "name": data[index]["name"],
                        "address": data[index]["address"],
                        "image": data[index]["images"].split(",")[0]
                    },
                    "date": data[index]["date"],
                    "time": data[index]["time"],
                    "price": data[index]["price"]
                }

            res = {
                "data" : data,
            }
            http_code = 200
            return jsonify(res), http_code
        
        except Exception as err:
            print(err)
            res = {
                "data" : None,
            }
            http_code = 200
            return jsonify(res), http_code

    # 新增行程
    elif request.method == "POST":
        input_data = request.get_json()

        try:
            input_data["attractionId"]
            command_paras = qry_para_set.booking_post(user_info["id"], input_data)
            data = flask_modules.query_create(command_paras)
            res = {"ok" : True}
            return jsonify(res), 200
        
        except Exception as err:
            print(err)
            msg = "建立失敗，輸入不正確或其他原因"
            res = {
                "error" : True,
                "message" : msg,
            }
            return jsonify(res), 400
        
    # 刪除行程
    elif request.method == "DELETE":
        input_data = request.get_json()
        try:
            command_paras = qry_para_set.booking_del(user_info["id"], input_data)
            data = flask_modules.query_del(command_paras)
            res = {
                "ok" : True,
            }
            return jsonify(res), 200

        except Exception as err:
            print(err)
            msg = "刪除失敗，異常輸入"
            res = {
                "error" : True,
                "message" : msg,
            }
            return jsonify(res), 400