from sub_functions.module_data import get_connect
from sub_functions.module_data import module_init_program
from sub_functions import qry_para_set_db_constructor


# Create_Table
# 之後改成 for loop 於開始前驗證個別是否存在
def create_table_controller(db_connection_pool):
    paras_table_mrts = qry_para_set_db_constructor.create_table_mrts()
    module_init_program.create_table(db_connection_pool, paras_table_mrts)
    paras_table_cats = qry_para_set_db_constructor.create_table_cats()
    module_init_program.create_table(db_connection_pool, paras_table_cats)

    # need FK to mrt & cat
    paras_table_attractions = qry_para_set_db_constructor.create_table_attractions()
    module_init_program.create_table(db_connection_pool, paras_table_attractions)

    # need FK to attractions & idpt
    paras_table_files = qry_para_set_db_constructor.create_table_files()
    module_init_program.create_table(db_connection_pool, paras_table_files)
    paras_table_locs = qry_para_set_db_constructor.create_table_locs()
    module_init_program.create_table(db_connection_pool, paras_table_locs)
    paras_table_weird_data = qry_para_set_db_constructor.create_table_weird_data()
    module_init_program.create_table(db_connection_pool, paras_table_weird_data)

    # 註冊用
    paras_table_auth = qry_para_set_db_constructor.create_table_auth()
    module_init_program.create_table(db_connection_pool, paras_table_auth)

    # booking
    paras_table_booking = qry_para_set_db_constructor.create_table_booking()
    module_init_program.create_table(db_connection_pool, paras_table_booking)

    # order
    paras_table_orders = qry_para_set_db_constructor.create_table_orders()
    module_init_program.create_table(db_connection_pool, paras_table_orders)

    # order detail
    paras_table_orders_detail = qry_para_set_db_constructor.create_table_orders_detail()
    module_init_program.create_table(db_connection_pool, paras_table_orders_detail)
    

def main():
    db_connection_pool = get_connect.access_db()
    db_name = "website_taipei"
    paras_db_exist = qry_para_set_db_constructor.check_db_exist(db_name)     
    if not module_init_program.check_db_exist(db_connection_pool, paras_db_exist):
        paras_create_db = qry_para_set_db_constructor.create_db_controller(db_name)
        module_init_program.create_db(db_connection_pool, paras_create_db)

    db_connection_pool.set_config(database=db_name)
    create_table_controller(db_connection_pool)


