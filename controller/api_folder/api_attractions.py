from flask import ( Blueprint, request, jsonify)

import module.operate_db as operate_db
from controller import qry_para_set


blueprint_attractions = Blueprint('blueprint_attractions', __name__, url_prefix ="/api")


# 取得景點列表資料(輸出 12 筆)
@blueprint_attractions.route("/attractions", methods=["GET"])
def attractions_list():
    try:
        page = int(request.args.get("page"))
        keyword = request.args.get("keyword")
        
        # 防止使用者亂搞
        if page == None:
            raise ValueError

        command_paras = qry_para_set.attractions_list(page, keyword)
        data = operate_db.query_fetch_all(command_paras)
        # 跟 DB 要 13 筆資料，若資料數小於等於 12，則此輪為最後一輪
        if len(data) <= 12:
            page = None
        else:
            page += 1
            data.pop()

        for data_separated in data:
            data_separated["images"] = data_separated["images"].split(",")
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
    
    except Exception as err:
        print(err)
        res = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(res), 500


# 根據景點編號取得景點資料
@blueprint_attractions.route("/attraction/<int:attractionId>", methods=["GET"])
def attractions_one(attractionId):
    try:
        command_paras = qry_para_set.attractions_one(attractionId)
        data = operate_db.query_fetch_one(command_paras)
        data["images"] = data["images"].split(",")
        res = {
            "data" : data
            }

        if not res:
            raise ValueError
        return jsonify(res), 200
    
    except ValueError:
        res = {
            "error": True,
            "message": "景點編號不正確"
        }
        return jsonify(res), 400
    
    except Exception as err:
        print(err)
        res = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(res), 500
    

# 根據景點編號取得景點資料
@blueprint_attractions.route("/mrts", methods=["GET"])
def mrts_list():
    try:
        command_paras = qry_para_set.mrts_list()
        data = operate_db.query_fetch_all(command_paras)
        for index in range(len(data)):
            data[index] = data[index]["mrt"]
        res = {
            "data" : data
            }
        
        return jsonify(res), 200
    
    except Exception as err:
        print(err)
        res = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(res), 500