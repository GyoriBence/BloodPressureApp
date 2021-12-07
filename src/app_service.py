'''The brain of the application. This is where the magic happens'''
import io
from random import randint
from flask import render_template, send_file
from pymongo import MongoClient
import pymongo
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


client = MongoClient("mongodb+srv://"
                     "Beni:Beni123@pythonassignmentcluster.drgjd.mongodb.net/"
                     "PythonAssignmentDataBase?retryWrites=true&w=majority")
DATABASE = client["PythonAssignmentDataBase"]["Measurements"]

if DATABASE.count() == 0:
    ID_NUMBER = 1
else:
    ID_NUMBER = DATABASE.find_one({}, sort=[("_id", pymongo.DESCENDING)])["_id"] + 1

def get_measurements():
    '''Getting the data from Database'''
    # Inner validating
    if DATABASE.count() == 0:
        return "<h1>Database is empty!</h1>"

    collected = []
    systolic_values = []
    diastolic_values = []

    for record in DATABASE.find({}):
        collected.append(record)
        systolic_values.append(record["Values"]["Systolic"])
        diastolic_values.append(record["Values"]["Diastolic"])

    return render_template("template.html",
                           content=collected,
                           avgsys=np.mean(systolic_values),
                           minsys=np.min(systolic_values),
                           maxsys=np.max(systolic_values),
                           avgdia=np.mean(diastolic_values),
                           mindia=np.min(diastolic_values),
                           maxdia=np.max(diastolic_values))

def post_measurements(data):
    '''Posting data using JSON'''
    data_sys = data["Systolic"]
    data_dia = data["Diastolic"]

    # Inner validating
    if data_sys > 300 or data_sys < 50 or data_dia > 200 or data_dia < 10:
        return "<h1>Bad request!</h1><br><h3>A value is out of range!" \
               "(Sys: 50-300, Dia: 10-200)</h3>"

    global ID_NUMBER
    DATABASE.insert_one({"_id": ID_NUMBER, "Type": "Added-By-User", "Values": data})
    ID_NUMBER+=1

    return f"<h3>ID: {ID_NUMBER-1}<br>Systolic: {data_sys}<br>Diastolic: {data_dia}<br>" \
           f"has been added to database!</h3>"

def get_image():
    '''Making barplot or lineplot based on the datas'''
    db_count = DATABASE.count()

    # Inner validating
    if db_count == 0:
        return "<h1>Database is empty!</h1>"

    database_helper = []

    for record in DATABASE.find({}):
        database_helper.append({"ID": record["_id"],
                                "Value Type": "Systolic",
                                "Value": record["Values"]["Systolic"]})
        database_helper.append({"ID": record["_id"],
                                "Value Type": "Diastolic",
                                "Value": record["Values"]["Diastolic"]})

    data_frame = pd.DataFrame(database_helper)
    sns.set()

    if db_count > 10:
        sns.lineplot(x="ID", y="Value", hue="Value Type", data=data_frame)
    else:
        sns.barplot(x="ID", y="Value", hue="Value Type", data=data_frame)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    
    return send_file(buf, mimetype="image/png")

def post_reset(data):
    '''Resetting database with x random data'''
    data_helper = data["Confirm"]
    data_random = data["No.Data"]

    # Inner validating
    if str(data_helper).lower() == "yes":
        if data_random < 0 or data_random > 100:
            return "<h1>Bad request!</h1><br><h3>Number of data is out of range! (1-100)</h3>"

        global ID_NUMBER
        ID_NUMBER = 1

        DATABASE.delete_many({})

        for index in range(0, data_random):
            DATABASE.insert_one({"_id": ID_NUMBER+index, "Type": "Auto-Generated", "Values":
                {"Systolic": randint(80, 220), "Diastolic": randint(50, 110)}})

        ID_NUMBER = data_random + 1
        return f"<h1>Database has been reset!</h1><br>" \
               f"<h3>{data_random} random data has been added to the database!</h3>"

    if str(data_helper).lower() == "no":
        return "<h1>Okay, see you later!</h1>"

    return "<h1>Bad request!</h1><br><h3>Invalid confirmation! (Yes/No)</h3>"
