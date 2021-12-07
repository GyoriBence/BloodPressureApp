'''Creating the core of the application'''
from flask import Flask
from src.app_controller import server_app

app = Flask(__name__)
app.register_blueprint(server_app)

@app.route("/", methods=["GET"])
def general_route():
    '''Creating main page'''
    return "<h1>Blood Pressure App</h1><br><h3>Győri Bence Zsolt - C01CLY</h3>"
