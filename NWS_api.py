from flask import Flask, jsonify
from Data.SQLite import SQLiteconn
import sqlite3

app = Flask(__name__)

DB_PATH = "C:\sources\BTDWA\Data\weather.db"

@app.route("/observations", methods = ["GET"])
def get_current_obs():
    
    with SQLiteconn(DB_PATH) as SQConn:
        obs = SQConn.getAllCachedNWSObservations()
        
        return jsonify(obs)
        
if __name__ == "__main__":
    app.run(debug=True)