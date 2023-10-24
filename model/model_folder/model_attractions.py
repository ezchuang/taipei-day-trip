import model.operate_db as operate_db
from model.model_folder import qry_para_set
# import qry_para_set


def attractions_list(page, keyword):
    command_paras = qry_para_set.attractions_list(page, keyword)
    data = operate_db.query_fetch_all(command_paras)
    return data


def attractions_one(attractionId):
    command_paras = qry_para_set.attractions_one(attractionId)
    data = operate_db.query_fetch_one(command_paras)
    return data
    

def mrts_list():
    command_paras = qry_para_set.mrts_list()
    data = operate_db.query_fetch_all(command_paras)
    return data