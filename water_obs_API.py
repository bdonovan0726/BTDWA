from flask import Flask, jsonify, request
from Data.SQLite import SQLiteconn
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)

DB_PATH = "Data/weather.db"

@app.route("/CurrentWaterObs", methods = ["GET"])
def get_current_water_obs():
    with SQLiteconn("Data/weather.db") as SQConn:
        obs, desc = SQConn.getWaterStationCacheInfo()
        jsonObs = [SQConn.rowToDict(desc, row) for row in obs]
        for row in jsonObs:
            row["ObsTimestamp"] = json.loads(row["ObsTimestamp"])
        return jsonify(jsonObs)
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5016, debug=True)