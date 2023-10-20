from flask import ( Blueprint, request, jsonify)

from modal.modal_folder import modal_attractions


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

        data = modal_attractions.attractions_list(page, keyword)

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
        data = modal_attractions.attractions_one(attractionId)

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
        data = modal_attractions.mrts_list()
        
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