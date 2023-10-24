from sub_functions.model_data import get_connect
from sub_functions.model_data import model_init_program
from sub_functions import qry_para_set_db_constructor


# Create_Table
# 之後改成 for loop 於開始前驗證個別是否存在
def create_table_controller(db_connection_pool):
    paras_table_mrts = qry_para_set_db_constructor.create_table_mrts()
    model_init_program.create_table(db_connection_pool, paras_table_mrts)
    paras_table_cats = qry_para_set_db_constructor.create_table_cats()
    model_init_program.create_table(db_connection_pool, paras_table_cats)

    # need FK to mrt & cat
    paras_table_attractions = qry_para_set_db_constructor.create_table_attractions()
    model_init_program.create_table(db_connection_pool, paras_table_attractions)

    # need FK to attractions & idpt
    paras_table_files = qry_para_set_db_constructor.create_table_files()
    model_init_program.create_table(db_connection_pool, paras_table_files)
    paras_table_locs = qry_para_set_db_constructor.create_table_locs()
    model_init_program.create_table(db_connection_pool, paras_table_locs)
    paras_table_weird_data = qry_para_set_db_constructor.create_table_weird_data()
    model_init_program.create_table(db_connection_pool, paras_table_weird_data)

    # 註冊用
    paras_table_auth = qry_para_set_db_constructor.create_table_auth()
    model_init_program.create_table(db_connection_pool, paras_table_auth)

    # booking
    paras_table_booking = qry_para_set_db_constructor.create_table_booking()
    model_init_program.create_table(db_connection_pool, paras_table_booking)

    # order
    paras_table_orders = qry_para_set_db_constructor.create_table_orders()
    model_init_program.create_table(db_connection_pool, paras_table_orders)

    # order detail
    paras_table_orders_detail = qry_para_set_db_constructor.create_table_orders_detail()
    model_init_program.create_table(db_connection_pool, paras_table_orders_detail)
    

def main():
    db_connection_pool = get_connect.access_db()
    db_name = "website_taipei"
    paras_db_exist = qry_para_set_db_constructor.check_db_exist(db_name)     
    if not model_init_program.check_db_exist(db_connection_pool, paras_db_exist):
        paras_create_db = qry_para_set_db_constructor.create_db_controller(db_name)
        model_init_program.create_db(db_connection_pool, paras_create_db)

    db_connection_pool.set_config(database=db_name)
    create_table_controller(db_connection_pool)


