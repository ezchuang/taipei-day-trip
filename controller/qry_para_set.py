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