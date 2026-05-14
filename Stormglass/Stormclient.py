import requests
import yaml
import arrow
import json
from datetime import datetime, timedelta, UTC

class StormGlass:

    def __init__(self, config_file : str):
        configs = yaml.safe_load(open(config_file))
        self.baseURL = 'https://api.stormglass.io/v2/weather/point'
        self.api_key = configs['stormglass']
        # self.reqParams = ['waveHeight', 'wavePeriod', 'waveDirection', 'windSpeed', 'windDirection',
                          # 'airTemperature', 'pressure', 'cloudCover', 'currentDirection', 'currentSpeed',
                          # 'gust', 'precipitation', 'swellDirection', 'rain', 'swellHeight', 'swellPeriod',
                          # 'secondarySwellPeriod', 'secondarySwellDirection', 'secondarySwellHeight',
                          # 'waterTemperature', 'surfaceTemperature', 'windWaveDirection', 'windWaveHeight',
                          # 'windWavePeriod']
        self.reqParams = ['airTemperature', 'pressure', 'cloudCover', 'gust', 'humidity',
                            'precipitation', 'rain', 'snow', 'windDirection', 'windSpeed']
                            
        self.reqPrecipParams = ['precipitation', 'rain', 'snow']
        
    def getStormglassForecast(self, lat : float, lon : float, itvDays = 7):
        start = datetime.now(UTC)
        end = start + timedelta(days=itvDays)
        print(f'Begin: {start}')
        print(f'End: {end}')
        response = requests.get(self.baseURL,
        params = {
            'lat' : lat,
            'lng' : lon,
            'params' : ','.join(self.reqParams),
            'start' : start.timestamp(),
            'end' : end.timestamp()
        },
        headers = {
            'Authorization' : self.api_key
        }
        )
        
        json_data = response.json()
        return json_data
        #print(json.dumps(json_data, indent = 2))
        
    def getStormglassHistoricalPrecipData(self, lat : float, lon : float):
        start = datetime.now(UTC) - timedelta(days=7)
        end = datetime.now(UTC)
        print(f'Historical Begin: {start}')
        print(f'Historical End: {end}')
        response = requests.get(self.baseURL,
        params = {
            'lat' : lat,
            'lng' : lon,
            'params' : ','.join(self.reqPrecipParams),
            'start' : start.timestamp(),
            'end' : end.timestamp()
        },
        headers = {
            'Authorization' : self.api_key
        }
        )
        
        json_data = response.json()
        return json_data