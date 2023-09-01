import get_connect
import module


# Create DB
def create_db_controller(db_connection_pool, db_name) -> bool:
    construct_paras = {
        "db_name" : f'{db_name}',
        "default" : "CHARACTER SET utf8mb4",
    }
    if not module.create_db(db_connection_pool, construct_paras):
        return False
    return True


def create_table_mrts(db_connection_pool) -> bool:
    construct_paras = {
        "table_name" : "mrts",
        "columns" : {
            "id" : "BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT",
            "mrt" : "VARCHAR(255)",
        }
    }
    if not module.create_table(db_connection_pool, construct_paras):
        return False
    return True


def create_table_cats(db_connection_pool) -> bool:
    construct_paras = {
        "table_name" : "cats",
        "columns" : {
            "id" : "BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT",
            "cat" : "VARCHAR(255)",
        }
    }
    if not module.create_table(db_connection_pool, construct_paras):
        return False
    return True


def create_table_attractions(db_connection_pool) -> bool:
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
    if not module.create_table(db_connection_pool, construct_paras):
        return False
    return True


def create_table_files(db_connection_pool) -> bool:
    construct_paras = {
        "table_name" : "files",
        "columns" : {
            "id" : "BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT",
            "attractions_id" : "BIGINT UNSIGNED NOT NULL",
            "file_url" : "VARCHAR(255) NOT NULL",
        },
        "foreign_key" : {
            "attractions_id" : "attractions(id)",
        },
    }
    if not module.create_table(db_connection_pool, construct_paras):
        return False
    return True


def create_table_locs(db_connection_pool) -> bool:
    construct_paras = {
        "table_name" : "locs",
        "columns" : {
            "id" : "BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT",
            "attractions_id" : "BIGINT UNSIGNED UNIQUE KEY NOT NULL",
            "direction" : "VARCHAR(5000) NOT NULL",
            "longitude" : "DOUBLE(8, 5) NOT NULL",
            "latitude" : "DOUBLE(7, 5) NOT NULL",
            "description" : "VARCHAR(5000) NOT NULL",
            "address" : "VARCHAR(255) NOT NULL",
        },
        "foreign_key" : {
            "attractions_id" : "attractions(id)",
        },
    }
    if not module.create_table(db_connection_pool, construct_paras):
        return False
    return True


def create_table_weird_data(db_connection_pool) -> bool:
    construct_paras = {
        "table_name" : "weird_data",
        "columns" : {
            "id" : "BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT",
            "attractions_id" : "BIGINT UNSIGNED UNIQUE KEY NOT NULL",
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
            "attractions_id" : "attractions(id)",
        },
    }
    if not module.create_table(db_connection_pool, construct_paras):
        return False
    return True


def create_table_auth(db_connection_pool) -> bool:
    construct_paras = {
        "table_name" : "auth",
        "columns" : {
            "id" : "BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT",
            "username" : "VARCHAR(255) UNIQUE KEY NOT NULL",
            "password" : "VARCHAR(255) NOT NULL",
            "name" : "VARCHAR(255) NOT NULL",
            "email" : "VARCHAR(255) NOT NULL",
        },
    }
    if not module.create_table(db_connection_pool, construct_paras):
        return False
    return True


# Create_Table
# 之後改成 for loop 於開始前驗證個別是否存在
def create_table_controller(db_connection_pool):
    create_table_mrts(db_connection_pool)
    create_table_cats(db_connection_pool)

    # need FK to mrt & cat
    create_table_attractions(db_connection_pool)

    # need FK to attractions & idpt
    create_table_files(db_connection_pool)
    create_table_locs(db_connection_pool)
    create_table_weird_data(db_connection_pool)

    # 註冊用
    create_table_auth(db_connection_pool)



if __name__ == "__main__":
    db_connection_pool = get_connect.create_pool()
    db_name = "website_taipei"
    if not module.check_db_exist(db_connection_pool, db_name):
        create_db_controller(db_connection_pool, db_name)
    db_connection_pool.set_config(database=db_name)
    create_table_controller(db_connection_pool)


