import json
import time
import logging
import os
import argparse
import requests
from NOAA.client import NOAAClient
from Data.SQLite import SQLiteconn
from datetime import datetime

parser = argparse.ArgumentParser()

parser.add_argument(
"-d", "--delay",
default = 900,
type = int,
help = 'time delay between fetches'
)

log_dir = "Logs"
os.makedirs(log_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = os.path.join(log_dir, f"weather_service_{timestamp}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]    
)

NDBC_URL = "https://www.ndbc.noaa.gov/data/realtime2/{}.txt"

def main():

    with SQLiteconn("Data/weather.db") as SQConn:
        
        waterStats = SQConn.getWaterStations()
        for stat in SQConn.getWaterStations():
            print(f'Station: {stat[0]}')
            buoyList = []
            tempDict = {
                        "WDIR" : [],
                        "WSPD" : [],
                        "GST" : [],
                        "WVHT" : [],
                        "DPD" : [],
                        "APD" : [],
                        "MWD" : [],
                        "PRES" : [],
                        "ATMP" : [],
                        "WTMP" : []
                        }

            for buoy in SQConn.getBuoysForWaterStation(stat[0]):
                buoyList.append(buoy[1])
                print(f'Getting buoy {buoy[1]}')
                bRawData = requests.get(NDBC_URL.format(buoy[1]))
                bLines = bRawData.text.splitlines()
                headers = bLines[0].split()
                data = bLines[2].split()
                tempData = dict(zip(headers, data))
                if tempData["WDIR"] != "MM":
                    tempDict["WDIR"].append(float(tempData["WDIR"]))
                if tempData["WSPD"] != "MM":
                    tempDict["WSPD"].append(float(tempData["WSPD"]))
                if tempData["GST"] != "MM":
                    tempDict["GST"].append(float(tempData["GST"]))
                if tempData["WVHT"] != "MM":
                    tempDict["WVHT"].append(float(tempData["WVHT"]))
                if tempData["DPD"] != "MM":
                    tempDict["DPD"].append(float(tempData["DPD"]))
                if tempData["APD"] != "MM":
                    tempDict["APD"].append(float(tempData["APD"]))
                if tempData["MWD"] != "MM":
                    tempDict["MWD"].append(float(tempData["MWD"]))
                if tempData["PRES"] != "MM":
                    tempDict["PRES"].append(float(tempData["PRES"]))
                if tempData["ATMP"] != "MM":
                    tempDict["ATMP"].append(float(tempData["ATMP"]))
                if tempData["WTMP"] != "MM":
                    tempDict["WTMP"].append(float(tempData["WTMP"]))      

            for k, v in tempDict.items():
                print(f'Key: {k} = Value: {v}')
                
            for k, v in tempDict.items():
                tempDict[k] = sum(tempDict[k])/len(tempDict[k])
                
            print("Now with averages:")
            
            for k, v in tempDict.items():
                print(f'Key: {k} = Value: {v}')
            
                
            #print(headers)
            
            
            
            
        
        
if __name__ == "__main__":
    
    try:
        while True:
            args = parser.parse_args()
            logging.info(f"Starting cycle with delay {args.delay} seconds...")
            try:
                main()
            except Exception as e:
                logging.error(f"Loop error: {e}")
                
            logging.info("Cycle complete. Sleeping...\n")
            time.sleep(args.delay)
            
    except Exception as e:
        logging.info(f"Caught exception: {e}")
        logging.info("Shutting down service gracefully...")