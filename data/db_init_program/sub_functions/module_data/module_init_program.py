from sub_functions.module_data import get_connect
"""
記得加上 Try error
execute() 有可能發生錯誤
"""


# decorator of CRUD
def preprocessing(func) -> bool:
    def wrapper(db_connection:object, db_cursor:object, paras:dict) -> bool:
        command = combine_query(func.__name__, paras)
        return func(db_connection, db_cursor, command, paras.get('target'))
    return wrapper


# process control of combine query 
def combine_query(func_name:str, paras:dict) -> str:
    if func_name == "check_db_exist":
        return combine_query_controller(func_name, paras)
    if func_name == "create_db":
        return combine_db_query(paras)
    if func_name == "create_table":
        return combine_table_query(paras)
    if func_name == "insert_data":
        return combine_create_query(paras)


def combine_general_query(paras:dict) -> str:
    if not paras.get("command"):
        return 
    
    res = f'{paras["command"]}'
    return res


def combine_db_query(paras:dict) -> str:
    if not paras.get("db_name"):
        return 
    
    res = f'CREATE DATABASE {paras["db_name"]}'
    if not paras.get("default"):
        return res
    res += f' DEFAULT {paras["default"]}'
    return res


def combine_table_query(paras:dict) -> str:
    if not paras.get("table_name") or not paras.get("columns"):
        return 
    
    cols = ""
    for column, attribute in paras.get("columns").items(): # 欄位組合
        cols += f' {column} {attribute},'
    
    if paras.get("unique"): # 複合唯一值
        unique_columns = ""
        for key_name, additions in paras.get("unique").items():
            unique_columns += f'CONSTRAINT {key_name}'

            for additions_item, additions_value in additions.items():
                if not additions_value:
                    continue

                if additions_item == "columns":
                    unique_columns += f' UNIQUE ({additions_value})'
                    continue
                unique_columns += f'{additions_item.upper()} {additions_value}'

            unique_columns += ","

        unique_columns = unique_columns[:-1] # 移除最後一個 ","
        cols += f'{unique_columns},'

    if paras.get("foreign_key"): # 外鍵
        for column, fk in paras.get("foreign_key").items():
            cols += f'FOREIGN KEY ({column}) REFERENCES {fk},'

    cols = cols[:-1]
    res = f'CREATE TABLE {paras.get("table_name")} ({cols})' # 加上最外圍的 table name
    return res


def combine_create_query(paras:dict) -> str:
    res = "INSERT INTO"
    if paras.get("table"):
        res += f" {paras['table']}"
    if paras.get("columns"):
        res += f" ( {paras['columns']} )"
    if paras.get("values"):
        res += f" VALUES ( {paras['values']} )"
    return res


# 決定 create DB 還是 Table <- 調整到 Query String Module
def combine_query_controller(func_name:str, paras:dict) -> str:
    if func_name == "create_table":
        return combine_table_query(paras)
    if func_name == "create_db":
        return combine_db_query(paras)


@get_connect.get_connection
@preprocessing
def check_db_exist(db_connection, db_cursor, command, target) -> bool:
    db_cursor.execute(command)
    db_name_arr = db_cursor.fetchall()
    return (target in db_name_arr)


@get_connect.get_connection
@preprocessing
def create_db(db_connection, db_cursor, command, target) -> bool:
    db_cursor.execute(command)
    db_connection.commit()
    return True


@get_connect.get_connection
@preprocessing
def create_table(db_connection, db_cursor, command, target) -> bool:
    db_cursor.execute(command)
    db_connection.commit()
    return True


@get_connect.get_connection
@preprocessing
def insert_data(connection, cursor, command, target) -> bool:
    cursor.execute(command, target)
    connection.commit()
    return True