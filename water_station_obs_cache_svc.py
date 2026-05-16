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
            for buoy in SQConn.getBuoysForWaterStation(stat[0]):
                buoyList.append(buoy[1])
                print(buoy[1])

            bRawData = requests.get(NDBC_URL.format(buoy[1]))
            headers = bRawData.text.splitlines()
            print(headers[0])
            
            
            
            
        
        
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