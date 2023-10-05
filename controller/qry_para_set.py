def attractions_list(page:int, keyword:str) -> str:
    command_paras = {
        "columns" : "attractions.id, \
            attractions.name, \
            cats.cat AS category, \
            locs.description, \
            locs.address, \
            locs.direction AS transport, \
            mrts.mrt, \
            locs.latitude AS lat, \
            locs.longitude AS lng, \
            GROUP_CONCAT(files.file_url SEPARATOR ',') AS images",
        "table" : "attractions LEFT JOIN mrts ON attractions.mrt_id = mrts.id \
            LEFT JOIN cats ON attractions.cat_id = cats.id \
            LEFT JOIN locs ON attractions.id = locs.attraction_id \
            LEFT JOIN files ON attractions.id = files.attraction_id",
        "where" : None,
        "group_by" : "attractions.id",
        "order_by" : None,
        "order_ordered" : None,
        "limit" : "%s, %s",
        "target" : (page*12, 13)
    }

    if not keyword:
        return command_paras
    command_paras["where"] = "attractions.name LIKE %s OR mrts.mrt = %s"
    command_paras["target"] = ("%" + keyword + "%", keyword, page*12, 12)
    return command_paras


def attractions_one(attractionId:int) -> str:
    command_paras = {
        "columns" : "attractions.id, \
            attractions.name, \
            cats.cat AS category, \
            locs.description, \
            locs.address, \
            locs.direction AS transport, \
            mrts.mrt, \
            locs.latitude AS lat, \
            locs.longitude AS lng, \
            GROUP_CONCAT(files.file_url) AS images",
        "table" : "attractions LEFT JOIN mrts ON attractions.mrt_id = mrts.id \
            LEFT JOIN cats ON attractions.cat_id = cats.id \
            LEFT JOIN locs ON attractions.id = locs.attraction_id \
            LEFT JOIN files ON attractions.id = files.attraction_id",
        "where" : "attractions.id = %s",
        "group_by" : "attractions.id",
        "order_by" : None,
        "order_ordered" : None,
        "limit" : None,
        "target" : (attractionId,)
    }
    return command_paras


def mrts_list() -> str:
    command_paras = {
        "columns" : "mrts.mrt",
        "table" : "attractions LEFT JOIN mrts ON attractions.mrt_id = mrts.id",
        "where" : None,
        "group_by" : "mrts.mrt",
        "order_by" : "count(mrts.mrt)",
        "order_ordered" : "DESC",
        "limit" : "%s",
        "target" : (40,)
    }
    return command_paras


def signup(data_signup:dict) -> str:
    data = (data_signup["name"],
            data_signup["email"],
            data_signup["password"],)
    command_paras = {"table": "auth",
                     "columns": "name, email, password",
                     "values": "%s, %s, %s",
                     "target" : data}
    return command_paras


def signin(email:int) -> str:
    command_paras = {
        "columns" : "id, name, email, password",
        "table" : "auth",
        "where" : "email = %s",
        "group_by" : None,
        "order_by" : None,
        "order_ordered" : None,
        "limit" : None,
        "target" : (email,)
    }
    return command_paras


def verify(decoded_data:dict):
    command_paras = {
        "columns" : "id, name, email",
        "table" : "auth",
        "where" : "id = %s AND name = %s AND email = %s",
        "group_by" : None,
        "order_by" : None,
        "order_ordered" : None,
        "limit" : None,
        "target" : (decoded_data["id"], decoded_data["name"], decoded_data["email"],)
    }
    return command_paras


def booking_get(user_id):
    # GROUP_CONCAT(files.file_url SEPARATOR ',') AS images,
    command_paras = {
        "columns" : "booking.id as booking_id, \
            booking.attraction_id as id, \
            attractions.name as name, \
            locs.address as address, \
            GROUP_CONCAT(files.file_url) AS images, \
            booking.date as date, \
            booking.time as time, \
            booking.price as price",
        "table" : "auth LEFT JOIN booking ON auth.id = booking.auth_id \
            LEFT JOIN attractions ON booking.attraction_id = attractions.id \
            LEFT JOIN locs ON attractions.id = locs.attraction_id \
            LEFT JOIN files ON attractions.id = files.attraction_id",
        "where" : "auth.id = %s",
        "group_by" : "booking.id",
        "order_by" : "booking.id",
        "order_ordered" : "ASC",
        "limit" : None,
        "target" : (user_id,)
    }
    return command_paras
    

def booking_post(user_id, input_data):
    data = (user_id,
            input_data["attractionId"],
            input_data["date"],
            input_data["time"],
            input_data["price"],)
    command_paras = {"table": "booking",
                     "columns": "auth_id, attraction_id, date, time, price",
                     "values": "%s, %s, %s, %s, %s",
                     "target" : data}
    return command_paras


def booking_del(user_id, input_data):
    data = (input_data["id"],
            user_id,)
    command_paras = {"table": "booking",
                     "where": "id = %s and auth_id = %s",
                     "target" : data}
    return command_paras


def booking_get_for_order(user_id):
    command_paras = {
        "columns" : "booking.id as booking_id, \
            booking.attraction_id as id, \
            booking.date as date, \
            booking.time as time, \
            booking.price as price",
        "table" : "auth LEFT JOIN booking ON auth.id = booking.auth_id",
        "where" : "auth.id = %s",
        "group_by" : None,
        "order_by" : "booking.id",
        "order_ordered" : "ASC",
        "limit" : None,
        "target" : (user_id,)
    }
    return command_paras


def orders_post_orders(order_id, user_id, input_data):
    data = (order_id,
            user_id,
            input_data["order"]["price"],
            input_data["order"]["contact"]["name"],
            input_data["order"]["contact"]["email"],
            input_data["order"]["contact"]["phone"],
            0)
    command_paras = {"table": "orders",
                     "columns": "order_id, auth_id, price, name, email, phone, order_status",
                     "values": "%s, %s, %s, %s, %s, %s, %s",
                     "target" : data}
    return command_paras


def orders_post_orders_detail(order_id, db_data_sep):
    data = (order_id,
            db_data_sep["id"],
            db_data_sep["date"],
            db_data_sep["time"],
            db_data_sep["price"])
    command_paras = {"table": "orders_detail",
                     "columns": "order_id, attraction_id, date, time, price",
                     "values": "%s, %s, %s, %s, %s",
                     "target" : data}
    return command_paras


def orders_set_delete_booking(user_id):
    data = (user_id,)
    command_paras = {"table": "booking",
                     "where": "auth_id = %s",
                     "target" : data}
    return command_paras


def orders_set_update_orders(order_id):
    data = (1, order_id,)
    command_paras = {"table": "orders",
                     "set": "order_status = %s",
                     "where": "order_id = %s",
                     "target" : data}
    return command_paras


def orders_get(user_id, order_id):
    command_paras = {
        "columns" : "orders.order_id as number, \
            orders.price as price, \
            orders_detail.attraction_id as id, \
            attractions.name as attraction_name, \
            locs.address as address, \
            GROUP_CONCAT(files.file_url) AS images, \
            orders_detail.date as date, \
            orders_detail.time as time, \
            orders.name as name, \
            orders.email as email, \
            orders.phone as phone, \
            orders.order_status as status",
        "table" : "auth LEFT JOIN orders ON auth.id = orders.auth_id \
            LEFT JOIN orders_detail ON orders.order_id = orders_detail.order_id \
            LEFT JOIN attractions ON orders_detail.attraction_id = attractions.id \
            LEFT JOIN locs ON attractions.id = locs.attraction_id \
            LEFT JOIN files ON attractions.id = files.attraction_id",
        "where" : "auth.id = %s and orders.order_id = %s",
        "group_by" : "orders_detail.id",
        "order_by" : "orders_detail.id",
        "order_ordered" : "ASC",
        "limit" : None,
        "target" : (user_id, order_id)
    }
    return command_paras


"""
OK 形式:

SELECT 
    attractions.id,
    attractions.name,
    cats.cat AS category,
    locs.description,
    locs.address,
    locs.direction AS transport,
    mrts.mrt,
    locs.latitude AS lat,
    locs.longitude AS lng,
    GROUP_CONCAT(files.file_url) AS images
FROM 
    attractions
LEFT JOIN 
    mrts ON attractions.mrt_id = mrts.id
LEFT JOIN 
    cats ON attractions.cat_id = cats.id
LEFT JOIN 
    locs ON attractions.id = locs.attraction_id
LEFT JOIN 
    files ON attractions.id = files.attraction_id
WHERE
	mrts.mrt = '關渡' OR attractions.name LIKE '%關渡'
GROUP BY
    attractions.id
ORDER BY
	attractions.id
LIMIT 0, 12;

"""