from flask import ( Blueprint, request, session, current_app,
                   request, jsonify)
import random, string

import jwt

import module.flask_modules as flask_modules
from controller import qry_para_set


# blueprint = Blueprint('blueprint123', __name__, url_prefix ="/api", static_folder="api", static_url_path="/api")
blueprint = Blueprint('blueprint123', __name__, url_prefix ="/api")
blueprint.static_folder = "api"

secret_key = "".join(random.choice(string.ascii_letters + string.digits) for i in range(20))


# api 全部都需要驗證
# @blueprint.before_request
# def before_request_bp():
#     if not session.get("signin"):
#         res = {
#             "error": True,
#             "message": "尚未登入"
#         }
#         return jsonify(res), 400


# def token_required(func):
#     @wrap(func)
#     def wrap():
#         token = None
#         if "Authorization" in request.headers:
#             token = request.headers["Authorization"].split(" ")[1]
#         input_data = request.get_json()
#         if not token:
#             raise ValueError
#         decoded_data = jwt.decode(token, secret_key, algorithms="HS256")
#         command_paras = qry_para_set.verify(decoded_data)
#         data = flask_modules.query_fetch_one(command_paras)
#         if not data:
#             raise ValueError
#         res = {
#             "data": data
#         }
#         return jsonify(res), 200
#     return wrap


# 會員註冊
@blueprint.route("/user", methods=["POST"])
def signup():
    res = {}
    input_data = request.get_json()
    try:
        if not input_data.get("name") or \
            not input_data.get("password") or \
            not input_data.get("email"):
            raise ValueError
        
        command_paras = qry_para_set.signup(input_data)
        if not flask_modules.query_create(command_paras):
            raise ValueError
        res = {"ok": True}
        return jsonify(res), 200
    
    except ValueError:
        if not input_data.get("name"):
            msg = "請輸入使用者名稱"
        elif not input_data.get("password"):
            msg = "請輸入密碼"
        elif not input_data.get("email"):
            msg = "請輸入 e-mail"
        else:
            msg = "e-mail 重複申請"

        res = {
            "error": True,
            "message": msg,
            }
        return jsonify(res), 400
    
    except:
        res = {
            "error": True,
            "message": "伺服器內部錯誤",
            }
        return jsonify(res), 500
    

# 登入、驗證登入狀態
@blueprint.route("/user/auth", methods=["GET", "PUT"])
def signin():
    res = {}
    if request.method == "GET":
        token = request.headers.get("token")
        try:
            if not token:
                raise ValueError
            decoded_data = jwt.decode(token, secret_key, algorithms="HS256")
            command_paras = qry_para_set.verify(decoded_data)
            print(decoded_data)
            data = flask_modules.query_fetch_one(command_paras)
            print(data)
            if not data:
                raise ValueError
            res = {
                "data": data,
            }
            return jsonify(res), 200
        except:
            res = {
                "data": None,
            }
            return jsonify(res), 200

    elif request.method == "PUT":
        input_data = request.get_json()
        try:
            if not input_data.get("email") or \
                not input_data.get("password"):
                raise ValueError
            email = input_data.get("email")
            command_paras = qry_para_set.signin(email)
            data = flask_modules.query_fetch_one(command_paras)
            if not data or input_data.get("password") != data.get("password"):
                raise ValueError
            payload = {
                "id": data["id"],
                "name": data["name"],
                "email": data["email"],
            }
            token = jwt.encode(payload, secret_key, algorithm="HS256")
            res = {"token": token}
            return jsonify(res), 200
        
        except ValueError:
            if not input_data.get("email"):
                msg = "請輸入 e-mail"
            elif not input_data.get("password"):
                msg = "請輸入密碼"
            else:
                msg = "e-mail 或密碼錯誤"
            res = {
                "error": True,
                "message": msg
            }
            return jsonify(res), 400
        
        except:
            msg = "伺服器內部錯誤"
            res = {
                "error": True,
                "message": msg
            }
            return jsonify(res), 500





# 取得景點列表資料(輸出 12 筆)
@blueprint.route("/attractions", methods=["GET"])
def attractions_list():
    try:
        page = int(request.args.get("page"))
        keyword = request.args.get("keyword")
        
        # 使用者亂搞
        if page == None:
            raise ValueError

        command_paras = qry_para_set.attractions_list(page, keyword)
        data = flask_modules.query_fetch_all(command_paras)
        # 跟 DB 要 13 筆資料，若資料數小於等於 12，則此輪為最後一輪
        if len(data) <= 12:
            page = None
        else:
            page += 1
            data.pop()

        for data_separated in data:
            data["images"] = data["images"].split(",")
        res = {
            "nextPage" : page,
            "data" : data,
            }

        # 字串搜尋沒資料
        if not res["data"]:
            raise ValueError
        
        return jsonify(res), 200
    
    except ValueError:
        res = {
            "error": True,
            "message": "無此資料"
        }
        return jsonify(res), 400
    
    except:
        res = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(res), 500


# 根據景點編號取得景點資料
@blueprint.route("/attraction/<int:attractionId>", methods=["GET"])
def attractions_one(attractionId):
    try:
        command_paras = qry_para_set.attractions_one(attractionId)
        data = flask_modules.query_fetch_one(command_paras)
        data["images"] = data["images"].split(",")        
        res = {
            "data" : data
            }

        if not res:
            raise TypeError
        return jsonify(res), 200
    
    except TypeError:
        res = {
            "error": True,
            "message": "景點編號不正確"
        }
        return jsonify(res), 400
    
    except:
        res = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(res), 500
    

# 根據景點編號取得景點資料
@blueprint.route("/mrts", methods=["GET"])
def mrts_list():
    try:
        command_paras = qry_para_set.mrts_list()
        data = flask_modules.query_fetch_all(command_paras)
        for index in range(len(data)):
            data[index] = data[index]["mrt"]
        res = {
            "data" : data
            }
        
        return jsonify(res), 200
    
    except:
        res = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(res), 500