## 初始化 程式 與 模組安裝:

- ubuntu apt 更新: `sudo apt update`
- git 安裝:
  1.  git 安裝:
      - `sudo apt-get install git`
  2.  git 檔案抓取:
      - `git clone "git HTTPS"` maybe you need specific branch, add `--branch "branch name"` after the commend before.
      - Other way:
        - `git remote "git HTTPS"`
        - `git checkout "branch name"`
        - `git pull`
- Python 安裝:
  1.  Python 安裝:
      - `sudo apt-get install python3`
  2.  Python 版本檢查:
      - `python3 --version`
  3.  Python 套件管理工具：
      - `sudo apt update && sudo apt install python3-pip`
  4.  module 安裝:
      - `pip install -r requirements.txt`
      1. module 取出:
         - `pip freeze > requirements.txt `
- MySQL 安裝:
  1.  MySQL 安裝:
      - `sudo apt install mysql-server`
  2.  顯示 MySQL 的系統服務狀態:
      - `sudo systemctl status mysql`
  3.  修改身分驗證方式:
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
  3. init_db_infos.env 放在 root/data/db_init_program/sub_functions/model_data，內含以下項目:
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
