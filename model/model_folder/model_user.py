import model.operate_db as operate_db
from model.model_folder import qry_para_set


def signup(input_data):
    command_paras = qry_para_set.signup(input_data)
    data = operate_db.query_create(command_paras)
    return data


def verify(decoded_data):
    command_paras = qry_para_set.verify(decoded_data)
    data = operate_db.query_fetch_one(command_paras)
    return data


def signin(email):
    command_paras = qry_para_set.signin(email)
    data = operate_db.query_fetch_one(command_paras)
    return data