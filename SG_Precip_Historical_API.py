from flask import Flask, jsonify, request
from Data.SQLite import SQLiteconn
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)

DB_PATH = "Data/weather.db"

@app.route("/historicalPrecip", methods = ["GET"])
def get_forecast_for_station():
    with SQLiteconn("Data/weather.db") as SQConn:
        req_station = request.args.get("station").upper()
        if not req_station:
            return jsonify({"error" : "station parametert required"}), 400
        histData = SQConn.getSGHistoricalPrecipData(req_station)
        precipData = {"stationID" : req_station,
                      "Start" : histData[1],
                      "End" : histData[2],
                      "Total Precipitation" : histData[3],
                      "Last Precipitation" : histData[7]
                     }
        return jsonify(precipData)
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5012, debug=True)