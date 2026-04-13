import json
from NOAA.client import NOAAClient
from WeatherObjects.WObj import NOAAForecastPoint
from Data.SQLite import SQLiteconn


def main():
    client = NOAAClient()

    #Example: West Coast (you can change this later)
    # lat = 37.7749
    # lon = -122.4194
    #at my apartment in altamonte
    lat = 28.6647
    lon = -81.3656
    #in Texas County, MO, middle of nowhere far from cities
    # lat = 37.3516
    # lon = -91.8294
    username = "bdonovan0726@gmail.com"
    
    print("Getting user station info....")
    SQConn = SQLiteconn("C:\sources\BTDWA\Data\weather.db")
    userID = SQConn.getUserIDbyUserName(username)
    
    print(f"User ID: {userID}")

    print("\n--- HOURLY FORECAST ---")
    forecast = client.get_hourly_forecast(lat, lon)
    #print(json.dumps(forecast, indent=2))
    AltamonteObj = NOAAForecastPoint(forecast["properties"]["periods"][0])
    print(AltamonteObj.temp)

    # first = forecast["properties"]["periods"][0]
    # second = forecast["properties"]["periods"][5]

    # print(f"Time: {first['startTime']}")
    # print(f"Temp: {first['temperature']} {first['temperatureUnit']}")
    # print(f"Wind: {first['windSpeed']} {first['windDirection']}") 
    # print(f"Percip: {first['probabilityOfPrecipitation']['value']}")
    # print(f"Summary: {first['shortForecast']}")
    
    # print('\n')
    # print(f"Time: {second['startTime']}")
    # print(f"Temp: {second['temperature']} {second['temperatureUnit']}")
    # print(f"Wind: {second['windSpeed']} {second['windDirection']}") 
    # print(f"Percip: {second['probabilityOfPrecipitation']['value']}")
    # print(f"Summary: {second['shortForecast']}")

    # print("\n--- CURRENT OBSERVATION ---")
    # # Example station (you can swap this later)
    # station_id = "26026"

    # obs = client.get_latest_observation(station_id)
    # #print(json.dumps(obs, indent=2))
    # props = obs["properties"]

    # print(f"Temp: {props['temperature']['value']}")
    # print(f"Wind Speed: {props['windSpeed']['value']}")
    # print(f"Wind Direction: {props['windDirection']['value']}")


if __name__ == "__main__":
    main()
