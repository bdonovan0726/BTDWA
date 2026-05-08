from flask import Flask, jsonify
from Data.SQLite import SQLiteconn
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)

DB_PATH = "Data/weather.db"

with SQLiteconn("Data/weather.db") as SQConn:
    query = """SELECT RawJSON from SG_Land_Forecast_Cache where StationID = 'KSTL'"""
    forecastData = SQConn.runAdHocSelectQuery(query)
    jsonData = json.loads(forecastData[0][0])
    print(f'Air temp: {jsonData['hours'][0]['airTemperature']['sg']}')