from flask import current_app
import mysql.connector


# decorator get connection
def get_connection(func) -> bool:
    def wrapper(paras):
        try:
            db_pool = current_app.config['connection_pool']
            db_connection = db_pool.get_connection()
            db_cursor = db_connection.cursor(dictionary=True)
            print("OK")
            return func(db_connection, db_cursor, paras)
        except Exception as err:
            print(err)
            db_connection.rollback()
            return False
        finally:
            db_cursor.close()
            db_connection.close()
    return wrapper


def create_pool(db_config):
    db_connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="pool_1", pool_size=5, **db_config)
    return db_connection_pool
