import json

from sub_functions.module_data import get_connect
from sub_functions.module_data import module_init_program
import qry_para_set_data_washer


# controller
def assort_data(db_connection_pool, data) -> None:
    mrt_dict, mrt_arr, index_mrt = {}, [], 1
    cat_dict, cat_arr, index_cat = {}, [], 1
    attractions_arr, locs_arr, files_arr, weird_data_arr = [], [], [], []
    data_cluster = [mrt_arr, cat_arr, attractions_arr, locs_arr, files_arr, weird_data_arr]

    file_index, file_temp_arr = 0, []
    for item in data:
        # mrt 與 cat 資料要先比對後再輸入(因為須整併)，回傳 index 是為了更新下一輪 dict 的 key
        index_mrt = qry_para_set_data_washer.create_table_mrts(item, mrt_dict, mrt_arr, index_mrt)
        index_cat = qry_para_set_data_washer.create_table_cats(item, cat_dict, cat_arr, index_cat)
        # 依序建立表格資料
        qry_para_set_data_washer.create_table_attractions(item, mrt_dict, cat_dict, attractions_arr)
        qry_para_set_data_washer.create_table_locs(item, locs_arr)
        qry_para_set_data_washer.create_table_weird_data(item, locs_arr, weird_data_arr)
        # 切開 files url 字串形成 file_temp_arr 中的 sub arr
        file_index = qry_para_set_data_washer.create_table_locs(item, file_index, file_temp_arr)
    
    # 外面兩層 for loop 將檔案扁平化加入 files_arr
    for file_temp_arr_sub in file_temp_arr:
        for data in file_temp_arr_sub:
            file_index = qry_para_set_data_washer.create_table_locs(files_arr, data)

    # 將 data_cluster 中的 data_arr 中的 data 資料 依序加入 DB 中 (CREATE)
    for data_arr in data_cluster:
        for data in data_arr:
            temp_value = "%s," * (len(data))
            data["values"] = temp_value[:-1]
            module_init_program.insert_data(db_connection_pool, data)
        

def main():
    data_arr =[]
    db_connection_pool = get_connect.create_pool()
    db_name = "website_taipei"
    db_connection_pool.set_config(database=db_name)

    with open("./data/taipei-attractions.json", mode="r", encoding="utf-8") as raw_data:
        raw_data = json.load(raw_data)
        raw_data = raw_data.get("result")
        data_arr = raw_data.get("results")
    assort_data(db_connection_pool, data_arr)
        