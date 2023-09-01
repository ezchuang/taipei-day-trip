import ast
import os
from dotenv import load_dotenv
import mysql.connector

# get connection
def get_connection(func) -> bool:
    def wrapper(db_pool, paras):
        try:
            db_connection = db_pool.get_connection()
            db_cursor = db_connection.cursor(dictionary=True)
            return func(db_connection, db_cursor, paras)
        except Exception as err:
            print(err)
            db_connection.rollback()
            return False
        finally:
            db_cursor.close()
            db_connection.close()
    return wrapper


def create_pool():
    # get db config
    load_dotenv()
    # ast.literal_eval <- 以不會執行內文的方式，讀取並正確轉義 str 成其它其他 data type
    db_config = ast.literal_eval(os.getenv("config"))

    db_connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="pool_1", pool_size=5, **db_config)
    return db_connection_pool
