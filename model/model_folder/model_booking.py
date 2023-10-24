import model.operate_db as operate_db
from model.model_folder import qry_para_set


def booking_get(user_id):
    command_paras = qry_para_set.booking_get(user_id)
    data = operate_db.query_fetch_all(command_paras)
    return data
        

def booking_post(user_id, input_data):
    command_paras = qry_para_set.booking_post(user_id, input_data)
    data = operate_db.query_create(command_paras)
    return data
        

def booking_del(user_id, input_data):
    command_paras = qry_para_set.booking_del(user_id, input_data)
    data = operate_db.query_del(command_paras)
    return data