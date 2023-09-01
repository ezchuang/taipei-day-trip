import mysql.connector
import get_connect


def combine_create_query(paras:dict) -> str:
    res = "INSERT INTO"
    if paras.get("table"):
        res += f" {paras['table']}"
    if paras.get("columns"):
        res += f" ( {paras['columns']} )"
    if paras.get("values"):
        res += f" VALUES ( {paras['values']} )"
    return res


@get_connect.get_connection
def insert_data(connection, cursor, data_arr:list) -> bool:
    for data in data_arr:
        target = data["target"]
        temp_value = ""
        for item in target:
            temp_value += "%s,"
        data["values"] = temp_value[:-1]
        command = combine_create_query(data)
        cursor.execute(command, target)
        connection.commit()
    
    return True

