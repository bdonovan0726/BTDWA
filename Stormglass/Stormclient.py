import requests
import yaml
import arrow
import json

class StormGlass:

    def __init__(self, config_file : str):
        configs = yaml.safe_load(open(config_file))
        self.baseURL = 'https://api.stormglass.io/v2/weather/point'
        self.api_key = configs['stormglass']
        self.reqParams = ['waveHeight', 'wavePeriod', 'waveDirection', 'windSpeed', 'windDirection',
                          'airTemperature', 'pressure', 'cloudCover', 'currentDirection', 'currentSpeed',
                          'gust', 'precipitation', 'swellDirection', 'rain', 'swellHeight', 'swellPeriod',
                          'secondarySwellPeriod', 'secondarySwellDirection', 'secondarySwellHeight',
                          'waterTemperature', 'surfaceTemperature', 'windWaveDirection', 'windWaveHeight',
                          'windWavePeriod']
        
    def getStormglassForecast(self, lat : float, lon : float):
        start = arrow.now().floor('day')
        end = arrow.now().ceil('day')
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