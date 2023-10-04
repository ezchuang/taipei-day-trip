def check_db_exist(db_name):
    construct_paras = {
        "command" : "SHOW DATABASES",
        "target" : "website_taipei",
    }
    return construct_paras


# Create DB
def create_db_controller(db_name) -> bool:
    construct_paras = {
        "db_name" : f'{db_name}',
        "default" : "CHARACTER SET utf8mb4",
    }
    return construct_paras


def create_table_mrts() -> bool:
    construct_paras = {
        "table_name" : "mrts",
        "columns" : {
            "id" : "BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT",
            "mrt" : "VARCHAR(255)",
            "INDEX" : "mrt_index (mrt)",
        }
    }
    return construct_paras


def create_table_cats() -> bool:
    construct_paras = {
        "table_name" : "cats",
        "columns" : {
            "id" : "BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT",
            "cat" : "VARCHAR(255)",
            "INDEX" : "cat_index (cat)",
        }
    }
    return construct_paras


def create_table_attractions() -> bool:
    # rate 能加上下限?
    construct_paras = {
        "table_name" : "attractions",
        "columns" : {
            "id" : "BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT",
            "RowNumber" : "INT UNSIGNED UNIQUE KEY NOT NULL",
            "SERIAL_NO" : "BIGINT UNSIGNED UNIQUE KEY NOT NULL",
            "name" : "VARCHAR(150) NOT NULL",
            "rate" : "INT UNSIGNED DEFAULT 0",
            "mrt_id" : "BIGINT UNSIGNED",
            "cat_id" : "BIGINT UNSIGNED",
        },
        "foreign_key" : {
            "mrt_id" : "mrts(id)",
            "cat_id" : "cats(id)",
        },
    }
    return construct_paras



def create_table_files() -> bool:
    construct_paras = {
        "table_name" : "files",
        "columns" : {
            "id" : "BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT",
            "attraction_id" : "BIGINT UNSIGNED NOT NULL",
            "file_url" : "VARCHAR(255) NOT NULL",
            "INDEX" : "attraction_id_index (attraction_id)",
        },
        "foreign_key" : {
            "attraction_id" : "attractions(id)",
        },
    }
    return construct_paras

def create_table_locs() -> bool:
    construct_paras = {
        "table_name" : "locs",
        "columns" : {
            "id" : "BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT",
            "attraction_id" : "BIGINT UNSIGNED UNIQUE KEY NOT NULL",
            "direction" : "VARCHAR(5000) NOT NULL",
            "longitude" : "DOUBLE(8, 5) NOT NULL",
            "latitude" : "DOUBLE(7, 5) NOT NULL",
            "description" : "VARCHAR(5000) NOT NULL",
            "address" : "VARCHAR(255) NOT NULL",
        },
        "foreign_key" : {
            "attraction_id" : "attractions(id)",
        },
    }
    return construct_paras


def create_table_weird_data() -> bool:
    construct_paras = {
        "table_name" : "weird_data",
        "columns" : {
            "id" : "BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT",
            "attraction_id" : "BIGINT UNSIGNED UNIQUE KEY NOT NULL",
            "REF_WP" : "INT UNSIGNED",
            "langinfo" : "INT UNSIGNED NOT NULL",
            "MEMO_TIME" : "VARCHAR(5000)",
            "idpt" : "VARCHAR(150)",
            "POI" : "VARCHAR(30)",
            "date" : "DATE",
            "avBegin" : "DATE",
            "avEnd" : "DATE",
        },
        "foreign_key" : {
            "attraction_id" : "attractions(id)",
        },
    }
    return construct_paras


def create_table_auth() -> bool:
    construct_paras = {
        "table_name" : "auth",
        "columns" : {
            "id" : "BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT",
            # "username" : "VARCHAR(255) UNIQUE KEY NOT NULL",
            "name" : "VARCHAR(255) NOT NULL",
            "email" : "VARCHAR(255) UNIQUE NOT NULL",
            "password" : "VARCHAR(255) NOT NULL",
            # "INDEX" : "email_index (email)",
        },
    }
    return construct_paras


def create_table_booking() -> bool:
    construct_paras = {
        "table_name" : "booking",
        "columns" : {
            "id" : "BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT",
            "auth_id" : "BIGINT UNSIGNED NOT NULL",
            "attraction_id" : "BIGINT UNSIGNED NOT NULL",
            "date" : "VARCHAR(255) NOT NULL",
            "time" : "VARCHAR(255) NOT NULL",
            "price" : "INT NOT NULL",
            "INDEX" : "index_auth_id (auth_id)",
        },
        "unique" : {
            "unique_booking" : { # Constraint Key Name
                "columns": "auth_id, date, time", # Multiple Columns Name
                "using" : None, # Using Index 
                "where" : None, # Where, where the columns should be constrain
            },
        },
        "foreign_key" : {
            "auth_id" : "auth(id)",
            "attraction_id" : "attractions(id)",
        },
    }
    return construct_paras


def create_table_orders() -> bool:
    construct_paras = {
        "table_name" : "orders",
        # 測試一下auto increment
        "columns" : {
            "order_id" : "BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT",
            "auth_id" : "BIGINT UNSIGNED NOT NULL",
            "price" : "INT NOT NULL",
            "name" : "VARCHAR(255) NOT NULL",
            "email" : "VARCHAR(255) NOT NULL",
            "phone" : "VARCHAR(255) NOT NULL",
            "order_status" : "BOOLEAN NOT NULL",
        },
        "unique" : None,
        "foreign_key" : {
            "auth_id" : "auth(id)",
        },
    }
    return construct_paras


def create_table_orders_detail() -> bool:
    construct_paras = {
        "table_name" : "orders_detail",
        # 測試一下auto increment
        "columns" : {
            "id" : "BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT",
            "order_id" : "BIGINT UNSIGNED",
            "attraction_id" : "BIGINT UNSIGNED NOT NULL",
            "date" : "VARCHAR(255) NOT NULL",
            "time" : "VARCHAR(255) NOT NULL",
            "price" : "INT NOT NULL",
            "INDEX" : "index_order_id (order_id)",
        },
        "unique" : None,
        "foreign_key" : {
            "order_id" : "orders(order_id)",
            "attraction_id" : "attractions(id)",
        },
    }
    return construct_paras