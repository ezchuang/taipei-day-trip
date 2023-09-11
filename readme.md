# 使用方式
## 初始化
- 程式 與 模組安裝:
  1. ubuntu apt 更新: `sudo apt update`
  2. Python 安裝: 
     1. Python 安裝: 
         - `sudo apt-get install python3`
     2. Python 版本檢查: 
         - `python3 --version`
     3. Python 套件管理工具：
         - `sudo apt update && sudo apt install python3-pip`
     4. module 安裝:  
         - `pip -r requirements.txt`
        1. module 取出:  
            - `pip freeze > requirements.txt `
  3. MySQL 安裝: 
     1. MySQL 安裝:
         - `sudo apt install mysql-server`
     2. 顯示 MySQL 的系統服務狀態:
         - `sudo systemctl status mysql`
     3. 修改身分驗證方式:
         - `sudo mysql`
         - `ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '想要設定的密碼'; FLUSH PRIVILEGES;`

## 資料操作
- 資料庫初始化:
  1. 執行資料庫建立 & 資料匯入腳本: 
      - `sudo python3 /data/db_init_program/db_init_program.py`
  2. 執行資料庫建立: 
      - `Y/N`
  3. 資料匯入: 
      - `Y/N`

- 資料操作:
  1. 資料庫登入:
     - `sudo mysql -u root -p`
  2. Python 執行 (記得確認路徑):
     - `sudo python3 app.py`
  3. Python 背景執行 (記得確認路徑):
     - `sudo nohup python3 app.py &`
  4. 刪除背景執行:
     - `sudo -s`
     - `ps -u root`/`ps -ax` 不知道是否需要使用 `ps -lf -u root`
     - `kill '對象thread'`