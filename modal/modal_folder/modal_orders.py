import modal.operate_db as operate_db
from modal.modal_folder import qry_para_set


def orders_get_all(user_id):
    command_paras = qry_para_set.orders_get_all(user_id)
    data = operate_db.query_fetch_all(command_paras)
    return data


def booking_get_for_order(user_id):
    command_paras = qry_para_set.booking_get_for_order(user_id)
    data = operate_db.query_fetch_all(command_paras)
    return data


def orders_post_orders(order_id, user_id, input_data):
    command_paras = qry_para_set.orders_post_orders(order_id, user_id, input_data)
    data = operate_db.query_create(command_paras)
    return data


def orders_post_orders_detail(order_id, db_data_sep):
    command_paras = qry_para_set.orders_post_orders_detail(order_id, db_data_sep)
    data = operate_db.query_create(command_paras)
    return data


def orders_set_delete_booking(user_id):
    command_paras = qry_para_set.orders_set_delete_booking(user_id)
    data = operate_db.query_del(command_paras)
    return data


def orders_set_update_orders(order_id):
    command_paras = qry_para_set.orders_set_update_orders(order_id)
    data = operate_db.query_update(command_paras)
    return data


def orders_get(user_id, order_id):
    command_paras = qry_para_set.orders_get(user_id, order_id)
    data = operate_db.query_fetch_all(command_paras)
    return data