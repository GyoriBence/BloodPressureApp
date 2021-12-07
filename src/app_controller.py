'''Application's route controlling part'''
from flask import Blueprint, request
import src.app_service as srvc

server_app = Blueprint("app-controller", __name__)

@server_app.route("/measurements", methods=["GET"])
def get_data():
    '''Casual data-returning method'''
    return srvc.get_measurements()

@server_app.route("/measurements", methods=["POST"])
def post_data():
    '''Posting data to the database using JSON format'''
    # Outer validating
    try:
        return srvc.post_measurements(request.json)
    except:
        return "<h1>Bad request!</h1><br><h3>Not valid JSON request!</h3>" \
               "<br>Try: {'Systolic': 100, 'Diastolic':70}"

@server_app.route("/image", methods=["GET"])
def get_img():
    '''Returning plots of the data'''
    return srvc.get_image()

@server_app.route("/reset", methods=["POST"])
def reset():
    '''Resetting a database with x random datas'''
    # Outer validating
    try:
        return srvc.post_reset(request.json)
    except:
        return "<h1>Bad request!</h1><br><h3>Not valid JSON request!</h3><br>" \
               "Try: {'Confirm': 'Yes', 'No.Data':5}"
