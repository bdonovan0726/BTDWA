import json
from NOAA.client import NOAAClient
from WeatherObjects.WObj import NOAAForecastPoint
from Data.SQLite import SQLiteconn
from NDBC.NDBCObj import NDBCBuoyData
from NDBC.NDBCClient import NDBCClient


def main():
    NDBCcli = NDBCClient()
    #firstBuoyDat = NDBCBuoyData(NDBCcli.getBuoyData("46042"))
    NDBCcli.getBuoyData("46042")
    # client = NOAAClient()
    # username = "bdonovan0726@gmail.com"
    # #Example: West Coast (you can change this later)
    # # lat = 37.7749
    # # lon = -122.4194
    # #at my apartment in altamonte
    # # lat = 28.6647
    # # lon = -81.3656
    # #in Texas County, MO, middle of nowhere far from cities
    # # lat = 37.3516
    # # lon = -91.8294
    # userStationsList = []
    # stationForecasts = []
    
    # print("Getting user station info....")
    # #SQConn = SQLiteconn("C:\sources\BTDWA\Data\weather.db")
    # with SQLiteconn("C:\sources\BTDWA\Data\weather.db") as SQConn:
        # userID = SQConn.getUserIDbyUserName(username)
    
        # print(f"User ID: {userID}")
        # print("Getting station ID' for user")
    
        # userStationIDs = SQConn.getStationsForUser(userID)
    
        # if not userStationIDs:
            # return
    
        # for statID in userStationIDs:
            # print(f"Found station {statID[0]} for user")
            
            # stationInfo = SQConn.getStationInfoByID(statID[0])
            # if not stationInfo:
                # print(f"Unable to locate information from station {statID[0]}")
                # return
            # userStationsList.append((stationInfo[1], stationInfo[4], stationInfo[5]))
    # #exiting the sql connection since no longer needed 
    # #i need to implement some UML modeling
    # for station in userStationsList:
        # print(f"Found info: {station}, calling weather API with coordinates {station[1]}, {station[2]}")
        # statForecastJSON = client.get_hourly_forecast(station[1], station[2])
        # stationForecasts.append(NOAAForecastPoint(statForecastJSON["properties"]["periods"][0], station[0]))

    # for forecast in stationForecasts:
        # print(f"Current forecast at {forecast.stationID} as of {forecast.startTime}:")
        # print(f"")
        # print(f"{forecast.shortFore}, {forecast.temp}{forecast.tempUnit} with winds {forecast.windSpeed} at {forecast.windDir}")
        # print(f"Humidity {forecast.humidity}")
        # print()



    # print("\n--- HOURLY FORECAST ---")
    # forecast = client.get_hourly_forecast(lat, lon)
    # #print(json.dumps(forecast, indent=2))
    # AltamonteObj = NOAAForecastPoint(forecast["properties"]["periods"][0])
    # print(AltamonteObj.temp)

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
    # station_id = "kgry"

    # obs = client.get_latest_observation(station_id)
    # print(json.dumps(obs, indent=2))
    # props = obs["properties"]

    # print(f"Temp: {props['temperature']['value']}")
    # print(f"Wind Speed: {props['windSpeed']['value']}")
    # print(f"Wind Direction: {props['windDirection']['value']}")


if __name__ == "__main__":
    main()
