import get_connect
"""
記得加上 Try error
execute() 有可能發生錯誤
"""

def combine_db_query(paras:dict) -> (bool, str):
    if not paras.get("db_name"):
        return (False, "")
    
    res = f'CREATE DATABASE {paras["db_name"]}'
    if not paras.get("default"):
        return (True, res)
    res += f' DEFAULT {paras["default"]}'
    return (True, res)


def combine_table_query(paras:dict) -> (bool, str):
    if not paras.get("table_name") or not paras.get("columns"):
        return (False, "")
    
    cols = ""
    for column, attribute in paras.get("columns").items():
        cols += f' {column} {attribute},'
    
    if paras.get("foreign_key"):
        for column, fk in paras.get("foreign_key").items():
            cols += f'FOREIGN KEY ({column}) REFERENCES {fk},'

    cols = cols[:-1]
    res = f'CREATE TABLE {paras.get("table_name")} ({cols})'
    return (True, res)


def combine_query_controller(func_name:str, paras:dict) -> (bool, str):
    if func_name == "create_table":
        return combine_table_query(paras)
    if func_name == "create_db":
        return combine_db_query(paras)


@get_connect.get_connection
def check_db_exist(db_pool, db_cursor, db_name:str) -> bool:
    db_cursor.execute("SHOW DATABASES")
    db_name_arr = db_cursor.fetchall()
    return (db_name in db_name_arr)


@get_connect.get_connection
def create_db(db_connection, db_cursor, paras:dict) -> bool:
    success, command = combine_query_controller("create_db", paras)
    # print(command)
    if not success:
        print("err is occur")
        return False
    db_cursor.execute(command)
    db_connection.commit()
    return True


@get_connect.get_connection
def create_table(db_connection, db_cursor, paras:dict) -> bool:
    success, command = combine_query_controller("create_table", paras)
    # print(command)
    if not success:
        print("err is occur")
        return False
    db_cursor.execute(command)
    db_connection.commit()
    return True