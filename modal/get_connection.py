import os
from dotenv import load_dotenv
from flask import current_app
import mysql.connector


# decorator get connection
def get_connection(func) -> bool:
    def wrapper(paras):
        try:
            db_pool = current_app.config['connection_pool']
            db_connection = db_pool.get_connection()
            db_cursor = db_connection.cursor(dictionary=True)
            return func(db_connection, db_cursor, paras)
        except Exception as err:
            print(err)
            print(type(err))
            db_connection.rollback()
            return False
        finally:
            db_cursor.close()
            db_connection.close()
    return wrapper


# 建立 pool
def create_pool(db_config):
    db_connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="pool_1", pool_size=5, **db_config)
    return db_connection_pool


# 建立 與 DB 的連線(嘗試密碼)
def access_db():
    dotenv_path = 'db_infos.env'
    load_dotenv(dotenv_path)
    try:
        db_config = {
            "host": os.getenv("HOST"),
            "username": os.getenv("DB_USERNAME"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DATABASE"),
        }
        return create_pool(db_config)
    except mysql.connector.errors.ProgrammingError as err:
        if err.errno != 1045:
            return
        db_config["password"] = os.getenv("DB_PASSWORD_BACKUP")
        return create_pool(db_config)
    except Exception as err:
        print(err)