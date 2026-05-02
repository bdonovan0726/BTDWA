from flask import Flask, jsonify
from Data.SQLite import SQLiteconn
import sqlite3

app = Flask(__name__)

DB_PATH = "Data/weather.db"

@app.route("/observations", methods = ["GET"])
def get_current_obs():
    
    with SQLiteconn(DB_PATH) as SQConn:
        obs, desc = SQConn.getAllCachedNWSObservations()
        jsonObs = [SQConn.rowToDict(desc, row) for row in obs]
        return jsonify(jsonObs)
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)