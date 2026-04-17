import requests
from .NDBCObj import NDBCBuoyData

# url = "https://www.ndbc.noaa.gov/data/realtime2/46012.txt"

# resp = requests.get(url)

# lines = resp.text.splitlines()

# # filter out header lines
# data_lines = [line for line in lines if not line.startswith("#")]

# latest = data_lines[0]

# print(latest)

class NDBCClient:
    
    def __init__(self):
        self.realtimeURL = "https://www.ndbc.noaa.gov/data/realtime2/{}.txt"

    def getBuoyData(self, station_id: str):
        #url = f"https://www.ndbc.noaa.gov/data/realtime2/{station_id}.txt"
        response = requests.get(self.realtimeURL.format(station_id))
        response.raise_for_status()
        
        respLines = response.text.splitlines()
        headers = respLines[0].split()
        dataLines = [line for line in respLines if not line.startswith('#')]
        values = dataLines[0].split()
        # print(headers)
        # wdat = dict(zip(headers, values))
        # for k,v in wdat.items():
           # print(k + ": " + v)
        return NDBCBuoyData(dict(zip(headers, values)))
        #return wdat


