import ast, os
from dotenv import load_dotenv
from flask import *
import module.flask_modules as flask_modules

from module import get_connection

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.json.ensure_ascii = False

# get db config
load_dotenv()
# ast.literal_eval <- 以不會執行內文的方式，讀取並正確轉義 str 成其它其他 data type
db_config = ast.literal_eval(os.getenv("config"))
app.config['connection_pool'] = get_connection.create_pool(db_config)
flask_modules.register_blue(app)


# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


app.config["DEBUG"] = True
# app.run(host="0.0.0.0", port=3000)
app.run(port = 3000)