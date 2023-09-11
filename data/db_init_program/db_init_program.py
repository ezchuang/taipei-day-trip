"""
資料庫建立 與 資料匯入
"""

from data import db_constructor
from data import data_washer

create_db = None
while create_db not in ["Y", "N"]:
    create_db = input("是否新建表格(會自動偵測是否有對應資料庫) (Y/N)")
    print("別鬧，再輸入一次是否新建表格，跳出程式請用 ctrl + C ")

if create_db == "Y":
    try:
        db_constructor.main()
    except Exception as err:
        print(err)


create_data = None
while create_data not in ["Y", "N"]:
    create_data = input("是否匯入 .json 檔案 (Y/N)")
    print("別鬧，再輸入一次是否匯入 .json，跳出程式請用 ctrl + C ")
    
if create_data == "Y":
    try:
        data_washer.main()
    except Exception as err:
        print(err)