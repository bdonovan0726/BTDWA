from flask import Flask, jsonify, request
from Data.SQLite import SQLiteconn
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)

DB_PATH = "Data/weather.db"

@app.route("/waterStations", methods = ["GET"])
def get_stations():
    with SQLiteconn("Data/weather.db") as SQConn:
        statData = SQConn.getAllWaterStationsMeta()
        stations = []
        for st in statData:
            stn = {"Station ID" : st[0],
                   "Station Name" : st[1],
                   "Station Description" : st[2]
                  }
            stations.append(stn)
        return jsonify(stations)
        
@app.route("/waterStationForecast", methods = ["GET"])
def get_forecast_for_station():
    with SQLiteconn("Data/weather.db") as SQConn:
        req_station = request.args.get("station").upper()
        if not req_station:
            return jsonify({"error" : "station parametert required"}), 400
        statForecast =  SQConn.getWaterStationCacheForecastData(req_station)
        forecast = {"Station ID" : req_station,
                    "Fecth Timstamp" : statForecast[0],
                    "Forecast Start" : statForecast[1],
                    "Forecast End" : statForecast[2],
                    "Station Name" : statForecast[4],
                    "Main Wind Warning" : statForecast[5],
                    "Offshore Wind Lower" : statForecast[6],
                    "Offshore Wind Upper" : statForecast[7],
                    "Offshore Wind Yellow" : statForecast[8],
                    "Offshore Wind Red" : statForecast[9],                       
                    "Forecast Data" : json.loads(statForecast[3])}
        return jsonify(forecast)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5022, debug=True)        
        
        
        
        
        
        
        
        
        
        
        
        #req_station = request.args.get("station").upper()