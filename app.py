from flask import *

from controller.api_folder.api_user import blueprint_user
from controller.api_folder.api_attractions import blueprint_attractions
from controller.api_folder.api_booking import blueprint_booking
from controller.api_folder.api_orders import blueprint_orders
from modal import get_connection

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.static_folder="view"

app.json.ensure_ascii = False

app.config['connection_pool'] = get_connection.access_db()
app.register_blueprint(blueprint_user)
app.register_blueprint(blueprint_attractions)
app.register_blueprint(blueprint_booking)
app.register_blueprint(blueprint_orders)


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
@app.route("/orders")
def orders():
	return render_template("orders.html")


app.config["DEBUG"] = True
app.run(host="0.0.0.0", port=3000)