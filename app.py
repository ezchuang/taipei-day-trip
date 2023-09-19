from flask import *

from api import blueprint
from module import get_connection

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.static_folder="app_folder"

# secret_key = random.randint(1000000000, 9999999999)
app.json.ensure_ascii = False

# from flask_cors import CORS
# CORS(app)

app.config['connection_pool'] = get_connection.access_db()
app.register_blueprint(blueprint)


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
# app.run(port=3000)
app.run(host="0.0.0.0", port=3000)