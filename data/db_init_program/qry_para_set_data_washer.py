import re


# url 切分
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


def create_table_mrts(item, mrt_dict, mrt_arr, index_mrt):
    if item.get("MRT") in mrt_dict:
        return index_mrt
    mrt_dict[item["MRT"]] = index_mrt
    item_mrt = (index_mrt, item["MRT"])
    mrt_arr.append({"table": "mrts", 
                    "target" : item_mrt})
    return index_mrt + 1


def create_table_cats(item, cat_dict, cat_arr, index_cat):
    if item.get("CAT") not in cat_dict:
        return index_cat
    cat_dict[item["CAT"]] = index_cat
    item_cat = (index_cat, item["CAT"])
    cat_arr.append({"table": "cats", 
                    "target" : item_cat})
    return index_cat + 1

    
def create_table_attractions(item, mrt_dict, cat_dict, attractions_arr):
    item_attraction = (item["_id"],
                        item["RowNumber"],
                        item["SERIAL_NO"],
                        item["name"],
                        item["rate"],
                        mrt_dict[item["MRT"]],
                        cat_dict[item["CAT"]])
    attractions_arr.append({"table": "attractions", 
                            "target" : item_attraction})
    
    
def create_table_locs(item, locs_arr):
    item_locs = (item["_id"],
                    item["_id"],
                    item["direction"],
                    item["longitude"],
                    item["latitude"],
                    item["description"],
                    item["address"])
    locs_arr.append({"table": "locs", 
                        "target" : item_locs})
    

def create_table_weird_data(item, weird_data_arr):
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
    

def create_table_files_part1(item, file_index, file_temp_arr):
    file_index, temp_arr = cut_file_str(file_index, item["_id"], item["file"])
    file_temp_arr.append(temp_arr)
    return file_index


def create_table_files_part2(files_arr, data):
    files_arr.append({"table": "files", 
                      "target" : data})