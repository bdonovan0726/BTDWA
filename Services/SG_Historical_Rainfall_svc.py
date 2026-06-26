import json
import time
import logging
import os
import argparse
from Data.SQLite import SQLiteconn
from datetime import datetime, timedelta, UTC
from Stormglass.Stormclient import StormGlass

parser = argparse.ArgumentParser()

parser.add_argument(
"-d", "--delay",
default = 3600,
type = int,
help = 'time delay between fetches'
)

log_dir = "Logs"
os.makedirs(log_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = os.path.join(log_dir, f"SG_Forecast_cache_service_{timestamp}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]    
)

def main():
    
    SGCli = StormGlass('keys.apk')
    
    with SQLiteconn("Data/weather.db") as SQConn:
        stats = SQConn.getAllNWSLandStations()
        for s in stats:
            print(f'Retrieving/updating forecast information for station: {s[0]}')
            respJSON = SGCli.getStormglassHistoricalPrecipData(s[3], s[4])
            pTotal = 0.0
            sTotal = 0.0
            lastPTime = "NA"
            for h in respJSON['hours']:
                tPre= h['precipitation']['sg']
                pTotal += tPre
                if tPre > 0.1:
                    lastPTime = h['time']
            
            try:
                print(f'Saving precip to DB for station {s[0]}')
                SQConn.updateSGHistoricalPrecip((respJSON['meta']['start'], respJSON['meta']['end'],
                                                pTotal, 0, 0, json.dumps(respJSON), lastPTime, s[0]))
            except Exception as e:
                logging.error(f'Received error : {e}')
                continue
                
            print(f'Precip Totals: {str(pTotal)}')
            print(f'Last Precip: {lastPTime}')
            #print(respJSON)
        
if __name__ == "__main__":
    
    try:
        while True:
            args = parser.parse_args()
            logging.info(f"Starting SG Historical precipitation cache run with delay {args.delay} seconds..")
            try:
                main()
            
            except Exception as e:
                logging.error(f'Encountered error in hist precip cache run: {e}')
                
            logging.info(f'Caching cycle complete, sleeping...')
            time.sleep(args.delay)
        
    except Exception as e:
        logging.error(f'Caught exception {e}')
        logging.error(f'Shutting down gracefully')