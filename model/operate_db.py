from modal import get_connection
from modal import combine_query

# C
@get_connection.get_connection
@combine_query.preprocessing
def query_create(db_connection, db_cursor, command, target) -> bool:
    db_cursor.execute(command, target)
    db_connection.commit()
    return True


# R_fetch_one
@get_connection.get_connection
@combine_query.preprocessing
def query_fetch_one(db_connection, db_cursor, command, target) -> dict:
    db_cursor.execute("SET SESSION group_concat_max_len = 100000")
    db_cursor.execute(command, target)
    return db_cursor.fetchone()


# R_fetch_all
@get_connection.get_connection
@combine_query.preprocessing
def query_fetch_all(db_connection, db_cursor, command, target) -> dict:
    db_cursor.execute("SET SESSION group_concat_max_len = 100000")
    db_cursor.execute(command, target)
    return db_cursor.fetchall()


# U
@get_connection.get_connection
@combine_query.preprocessing
def query_update(db_connection, db_cursor, command, target) -> bool:
    db_cursor.execute(command, target)
    db_connection.commit()
    return True


# D
@get_connection.get_connection
@combine_query.preprocessing
def query_del(db_connection, db_cursor, command, target) -> bool:
    db_cursor.execute(command, target)
    db_connection.commit()
    return True