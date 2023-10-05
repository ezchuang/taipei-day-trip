from flask import ( Blueprint, request, jsonify)
from datetime import datetime, timedelta
# import random, string
import jwt

import module.flask_modules as flask_modules
from controller import qry_para_set


blueprint_user = Blueprint('blueprint_user', __name__, url_prefix ="/api")


secret_key = "oQAQByzarbxzNYSvuP3V4sdZyfKqxeHq"
# secret_key = "".join(random.choice(string.ascii_letters + string.digits) for i in range(32))


# 會員註冊
@blueprint_user.route("/user", methods=["POST"])
def signup():
    res = {}
    input_data = request.get_json()
    try:
        if not input_data.get("name") or \
            not input_data.get("email") or \
            not input_data.get("password"):
            raise ValueError
        
        command_paras = qry_para_set.signup(input_data)
        if not flask_modules.query_create(command_paras):
            raise ValueError
        res = {
            "ok" : True
            }
        return jsonify(res), 200
    
    except ValueError:
        if not input_data.get("name"):
            msg = "請輸入使用者名稱"
        elif not input_data.get("email") or "@" not in input_data["email"]:
            msg = "請輸入 e-mail"
        elif not input_data.get("password"):
            msg = "請輸入密碼"
        else:
            msg = "e-mail 重複申請"

        res = {
            "error" : True,
            "message" : msg,
            }
        return jsonify(res), 400
    
    except Exception as err:
        print(err)
        res = {
            "error" : True,
            "message" : "伺服器內部錯誤",
            }
        return jsonify(res), 500
    

# 登入、驗證登入狀態
@blueprint_user.route("/user/auth", methods=["GET", "PUT"])
def signin():
    res = {}

    # 驗證登入狀態
    if request.method == "GET":
        authorization = request.authorization
        try:
            if not authorization:
                raise ValueError
            token = authorization.token 
            # JWT Module會自動驗證過期時間
            decoded_data = jwt.decode(token, secret_key, algorithms="HS256")
            command_paras = qry_para_set.verify(decoded_data)
            data = flask_modules.query_fetch_one(command_paras)

            if not data:
                raise ValueError
            res = {
                "data" : data,
            }
            return jsonify(res), 200
        except Exception as err:
            print(err)
            res = {
                "data" : None,
            }
            return jsonify(res), 200

    # 登入
    elif request.method == "PUT":
        input_data = request.get_json()
        try:
            if not input_data.get("email") or \
                "@" not in input_data["email"] or \
                not input_data.get("password"):
                raise ValueError
            email = input_data.get("email")
            command_paras = qry_para_set.signin(email)
            data = flask_modules.query_fetch_one(command_paras)
            if not data or input_data.get("password") != data.get("password"):
                raise ValueError
            payload = {
                "id" : data["id"],
                "name" : data["name"],
                "email" : data["email"],
                "exp" : datetime.utcnow() + timedelta(days=7),
            }
            token = jwt.encode(payload, secret_key, algorithm="HS256")
            res = {"token" : token}
            return jsonify(res), 200
        
        except ValueError:
            if not input_data.get("email"):
                msg = "請輸入 e-mail"
            elif not input_data.get("password"):
                msg = "請輸入密碼"
            else:
                msg = "e-mail 或密碼錯誤"
            res = {
                "error" : True,
                "message" : msg
            }
            return jsonify(res), 400
        
        except Exception as err:
            print(err)
            msg = "伺服器內部錯誤"
            res = {
                "error" : True,
                "message" : msg
            }
            return jsonify(res), 500