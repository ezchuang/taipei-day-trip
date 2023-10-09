from flask import request
from functools import wraps
import jwt

from controller.api_folder.api_user import secret_key
import module.operate_db as operate_db
from controller import qry_para_set


def token_required(func):
    @wraps(func)
    def decorated():
        res = {}
        token = ""
        http_code = 0
        try:
            if "Authorization" in request.headers:
                authorization = request.authorization
                token = authorization.token
            if not token:
                raise ValueError
        
            decoded_data = jwt.decode(token, secret_key, algorithms="HS256")
            command_paras = qry_para_set.verify(decoded_data)
            data = operate_db.query_fetch_one(command_paras)

            if not data:
                raise ValueError
            
            http_code = 200
            res = data

            return func(res, http_code)
        
        except ValueError as err:
            print("ValueError ", err)
            msg = "未登入系統，拒絕存取"
            http_code = 403
            res = {
                "error" : True,
                "message": msg,
            }
            return func(res, http_code)
        
        except Exception as err:
            print("Exception ", err)
            msg = "伺服器內部錯誤"
            http_code = 500
            res = {
                "error" : True,
                "message": msg,
            }
            return func(res, http_code)
            
    return decorated


def token_required_special(func):
    @wraps(func)
    def decorated(order_id=None):
        res = {}
        token = ""
        http_code = 0
        try:
            if "Authorization" in request.headers:
                authorization = request.authorization
                token = authorization.token
            if not token:
                raise ValueError
        
            decoded_data = jwt.decode(token, secret_key, algorithms="HS256")
            command_paras = qry_para_set.verify(decoded_data)
            data = operate_db.query_fetch_one(command_paras)

            if not data:
                raise ValueError
            
            http_code = 200
            res = data

            return func(res, http_code, order_id)
        
        except ValueError as err:
            print("ValueError ", err)
            msg = "未登入系統，拒絕存取"
            http_code = 403
            res = {
                "error" : True,
                "message": msg,
            }
            return func(res, http_code, order_id)
        
        except Exception as err:
            print("Exception ", err)
            msg = "伺服器內部錯誤"
            http_code = 500
            res = {
                "error" : True,
                "message": msg,
            }
            return func(res, http_code, order_id)
            
    return decorated