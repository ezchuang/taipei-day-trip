from flask import ( Blueprint, request, session, current_app,
                   request, jsonify)

import module.flask_modules as flask_modules
from controller import qry_para_set


blueprint = Blueprint('blueprint123', __name__, url_prefix ="/api", static_folder="api", static_url_path="/api")


# api 全部都需要驗證
# @blueprint.before_request
# def before_request_bp():
#     if not session.get("signin"):
#         res = {
#             "error": True,
#             "message": "尚未登入"
#         }
#         return jsonify(res), 400


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
        datas = flask_modules.query_fetch_all(command_paras)
        # 跟 DB 要 13 筆資料，若資料數小於 12，則此輪為最後一輪
        if len(datas) < 12:
            page = None
        else:
            page += 1
            datas.pop()

        for data in datas:
            data["images"] = data["images"].split(",")
        res = {
            "nextPage" : page,
            "data" : datas,
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
@blueprint.route("/attractions/<int:attractionId>", methods=["GET"])
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
        datas = flask_modules.query_fetch_all(command_paras)
        for index in range(len(datas)):
            datas[index] = datas[index]["mrt"]
        res = {
            "data" : datas
            }
        
        return jsonify(res), 200
    
    except:
        res = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(res), 500