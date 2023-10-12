# 台北一日遊 網頁專案
- 前端架構使用 Flask render_template + html/CSS + JS
- 後端架構使用 Python + Flask + Python-mysql.connector + MySQL
- 認證使用 JWT (JSON Web Token)，加密用 HS256
- 付款用 Tap Pay 系統，無實質功能(可以測試付款，不會真的扣款)
- 採用 MVC 架構 + RestAPI 設計風格 + 盡可能朝 CSR 編撰
  
# 我的特色如下:
此為 Camp 的共同作業，我的這份特色如下:
1. 參數化 Raw SQL 指令，使用 Python script 建立 Schema and tables，且 Flask access API 時也套用同一套方法訪問資料庫。優點是: 
    - 用同一套系統管理資料架構，減少介面
    - 集中個別對於資料庫的動作參數，方便比較與修改
2. 目前 DB 中數據量不大，search (select) 時嘗試盡量減少 access DB 的次數，減少重複從 connection pool 中取得 connection 所花的 I/O 時間
3. 不使用框架完成圖片輪轉動畫

## 初始化 程式 與 模組安裝:
  - ubuntu apt 更新: `sudo apt update`
  - git 安裝: 
     1. git 安裝: 
         - `sudo apt-get install git`
     2. git 檔案抓取: 
         - `git clone "git HTTPS"` maybe you need specific branch, add `--branch "branch name"` after the commend before.
         - Other way:
           - `git remote "git HTTPS"`
           - `git checkout "branch name"`
           - `git pull`
  - Python 安裝: 
     1. Python 安裝: 
         - `sudo apt-get install python3`
     2. Python 版本檢查: 
         - `python3 --version`
     3. Python 套件管理工具：
         - `sudo apt update && sudo apt install python3-pip`
     4. module 安裝:  
         - `pip install -r requirements.txt`
        1. module 取出:  
            - `pip freeze > requirements.txt `
  - MySQL 安裝: 
     1. MySQL 安裝:
         - `sudo apt install mysql-server`
     2. 顯示 MySQL 的系統服務狀態:
         - `sudo systemctl status mysql`
     3. 修改身分驗證方式:
         - `sudo mysql`
         - `ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '想要設定的密碼'; FLUSH PRIVILEGES;`

## 資料操作
- 環境變數匯入
  1. db_info.env 放在 root，內含以下項目:
      - HOST
      - DB_USERNAME
      - DB_PASSWORD
      - DATABASE
  2. partner_key.env 放在 root，內含以下項目:
      - PARTNER_KEY
  3. init_db_infos.env 放在 root/data/db_init_program/sub_functions/module_data，內含以下項目:
      - HOST
      - DB_USERNAME
      - DB_PASSWORD
      - DATABASE

- 資料庫初始化:
  1. 執行資料庫建立 & 資料匯入腳本: 
      - `sudo python3 data/db_init_program/db_init_program.py`
  2. 執行資料庫建立: 
      - `Y/N`
  3. 資料匯入: 
      - `Y/N`

- 資料操作:
  1. 資料庫登入:
     - `sudo mysql -u root -p`
  2. 主程序執行 (記得確認路徑):
     - `sudo python3 app.py`
  3. 主程序背景執行 (記得確認路徑):
     - `sudo nohup python3 app.py &`
  4. 刪除背景執行:
     - `ps -ef`
       - `ps -ef | grep "你想撈的關鍵字"`
       - 其他指令參考: `ps -u root` / `ps -ax` / `ps -lf -u root`
     - `sudo kill '對象thread'`