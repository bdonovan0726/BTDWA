from flask import Flask, jsonify, request
from Data.SQLite import SQLiteconn
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)

DB_PATH = "Data/weather.db"

@app.route("/forecast", methods = ["GET"])
def get_forecast_for_station():
    with SQLiteconn("Data/weather.db") as SQConn:
        req_station = request.args.get("station").upper()
        if not req_station:
            return jsonify({"error" : "station parametert required"}), 400
        statForecast =  SQConn.getStationCacheForecastData(req_station)
        forecast = {"Station ID" : req_station,
                    "Fecth Timstamp" : statForecast[0],
                    "Forecast Start" : statForecast[1],
                    "Forecast End" : statForecast[2],
                    "Station Name" : statForecast[4],
                    "Station Description" : statForecast[5],
                    "Forecast Data" : statForecast[3]}
        return jsonify(forecast)
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5008, debug=True)
                    
    