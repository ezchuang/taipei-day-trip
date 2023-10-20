# decorator of CRUD
def preprocessing(func):
    def wrapper(db_connection, db_cursor, paras):
        command = combine_query(func.__name__, paras)
        return func(db_connection, db_cursor, command, paras.get('target'))
    return wrapper


# process control of combine query 
def combine_query(func_name, paras):
    if func_name == "query_create":
        return combine_create_query(paras)
    if func_name == "query_fetch_one" or func_name == "query_fetch_all":
        return combine_read_query(paras)
    if func_name == "query_update":
        return combine_update_query(paras)
    if func_name == "query_del":
        return combine_delete_query(paras)


# query combine create
def combine_create_query(paras):
    res = "INSERT INTO"
    if paras.get("table"):
        res += f" {paras['table']}"
    if paras.get("columns"):
        res += f" ( {paras['columns']} )"
    if paras.get("values"):
        res += f" VALUES ( {paras['values']} )"
    return res


# query combine read
def combine_read_query(paras):
    res = "SELECT"
    if paras.get("columns"):
        res += f" {paras['columns']}"
    if paras.get("table"):
        res += f" FROM {paras['table']}"
    if paras.get("where"):
        res += f" WHERE {paras['where']}"
    if paras.get("group_by"):
        res += f" GROUP BY {paras['group_by']}" 
    if paras.get("order_by"):
        res += f" ORDER BY {paras['order_by']}"
    if paras.get("order_ordered"):
        res += f" {paras['order_ordered']}"
    if paras.get("limit"):
        res += f" LIMIT {paras['limit']}"
    return res


# query combine update
def combine_update_query(paras):
    res = "UPDATE"
    if paras.get("table"):
        res += f" {paras['table']}"
    if paras.get("set"):
        res += f" SET {paras['set']}"
    if paras.get("where"):
        res += f" WHERE {paras['where']}"
    return res


# query combine delete
def combine_delete_query(paras):
    res = "DELETE"
    if paras.get("table"):
        res += f" FROM {paras['table']}"
    if paras.get("where"):
        res += f" WHERE {paras['where']}"
    return res