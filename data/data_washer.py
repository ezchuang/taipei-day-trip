import json
import re
import mysql.connector
import get_connect, module_data_washer


def cut_file_str(file_id:int, attraction_id:int, urls:str) -> list:
    pattern = r"https:"
    arr = re.split(pattern, urls)

    pattern = r"[jJ][pP][gG]"
    res = []
    for url in arr:
        if len(url) < 3:
            continue
        if not re.search(pattern, url[-3:]):
            continue
        file_id += 1
        res.append([file_id, attraction_id, "https:" + url])

    return file_id, res
    

# controller
def assort_data(db_connection_pool, data) -> None:
    mrt_dict, mrt_arr, index_mrt = {}, [], 1
    cat_dict, cat_arr, index_cat = {}, [], 1
    attractions_arr, locs_arr, files_arr, weird_data_arr = [], [], [], []
    data_cluster = [mrt_arr, cat_arr, attractions_arr, locs_arr, files_arr, weird_data_arr]

    file_index, file_temp_arr = 0, []
    for item in data:
        # get mrts
        if item.get("MRT") not in mrt_dict:
            mrt_dict[item["MRT"]] = index_mrt
            item_mrt = (index_mrt, item["MRT"])
            mrt_arr.append({"table": "mrts", 
                            "target" : item_mrt})
            index_mrt += 1
        # get cats
        if item.get("CAT") not in cat_dict:
            cat_dict[item["CAT"]] = index_cat
            item_cat = (index_cat, item["CAT"])
            cat_arr.append({"table": "cats", 
                            "target" : item_cat})
            index_cat += 1
        # get attractions
        item_attraction = (item["_id"],
                           item["RowNumber"],
                           item["SERIAL_NO"],
                           item["name"],
                           item["rate"],
                           mrt_dict[item["MRT"]],
                           cat_dict[item["CAT"]])
        attractions_arr.append({"table": "attractions", 
                                "target" : item_attraction})
        # get locs
        item_locs = (item["_id"],
                     item["_id"],
                     item["direction"],
                     item["longitude"],
                     item["latitude"],
                     item["description"],
                     item["address"])
        locs_arr.append({"table": "locs", 
                         "target" : item_locs})
        # get weird data
        item_weird_data = (item["_id"],
                           item["_id"],
                           item["REF_WP"],
                           item["langinfo"],
                           item["MEMO_TIME"],
                           item["idpt"],
                           item["POI"],
                           item["date"],
                           item["avBegin"],
                           item["avEnd"])
        weird_data_arr.append({"table": "weird_data", 
                               "target" : item_weird_data})
        # get files
        file_index, temp_arr = cut_file_str(file_index, item["_id"], item["file"])
        file_temp_arr += temp_arr

    for data in file_temp_arr:
        files_arr.append({"table": "files", 
                          "target" : data})
        
    for data_arr in data_cluster:
        module_data_washer.insert_data(db_connection_pool, data_arr)
        

if __name__ == "__main__":
    data_arr =[]
    db_connection_pool = get_connect.create_pool()
    db_name = "website_taipei"
    db_connection_pool.set_config(database=db_name)

    with open("./data/taipei-attractions.json", mode="r", encoding="utf-8") as raw_data:
        raw_data = json.load(raw_data)
        raw_data = raw_data.get("result")
        data_arr = raw_data.get("results")
    assort_data(db_connection_pool, data_arr)
        