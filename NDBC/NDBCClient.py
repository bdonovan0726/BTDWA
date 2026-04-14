import requests

url = "https://www.ndbc.noaa.gov/data/realtime2/46012.txt"

resp = requests.get(url)

lines = resp.text.splitlines()

# filter out header lines
data_lines = [line for line in lines if not line.startswith("#")]

latest = data_lines[0]

print(latest)