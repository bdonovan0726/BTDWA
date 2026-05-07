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
        
    def getStormglassForecast(self, lat : float, lon : float):
        start = datetime.now(UTC)
        end = start + timedelta(hours=3)
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
        print(json.dumps(json_data, indent = 2))