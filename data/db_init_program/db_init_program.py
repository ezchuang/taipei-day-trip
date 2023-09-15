"""
資料庫建立 與 資料匯入
"""

from sub_functions import db_constructor
from sub_functions import data_washer

create_db = None
create_db = input("是否新建表格(會自動偵測是否有對應資料庫) (Y/N)")
while create_db not in ["Y", "y", "N", "n"]:
    create_db = input("是否新建表格(會自動偵測是否有對應資料庫) (Y/N)")
    print("別鬧，再輸入一次是否新建表格，跳出程式請用 ctrl + C ")

if create_db in ["Y", "y"]:
    try:
        db_constructor.main()
    except Exception as err:
        print(err)


create_data = None
create_data = input("是否匯入 .json 檔案 (Y/N)")
while create_data not in ["Y", "y", "N", "n"]:
    create_data = input("是否匯入 .json 檔案 (Y/N)")
    print("別鬧，再輸入一次是否匯入 .json，跳出程式請用 ctrl + C ")
    
if create_data in ["Y", "y"]:
    try:
        data_washer.main()
    except Exception as err:
        print(err)