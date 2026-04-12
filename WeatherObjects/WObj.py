#generic weather objects

class WeatherNode:

	_isWaterNode = False
	_forecastObjList = []
	_stationID = ''
	
	
	
class NOAAForecastPoint:
    #this current implementation ties us to the NOAA JSON structure...this will break long term but for now we can use it
    #for now it is just easier to pass it a chunk of JSON, we will revisit this
	#def __init__(self, startTm : str, endTm : str, temp : int, tempUnit : str, precipProb : int, humid : int):#this is getting crazy, try something else
	def __init__(self, rawData : Dict[str, Any]):
		self.startTime = rawData["startTime"]
        self.endTime = rawData["endTime"]
        self.isDayTime = rawData["isDaytime"]
        self.temp = str(rawData["temperature"])
        self.tempUnit = str(rawData["temperatureUnit"]
        self.precipProb = str(rawData["probabilityOfPrecipitation"]["value"]
        self.humidity = str(rawData["relativeHumidity"]["value"])
        self.windSpeed = rawData["windSpeed"]
        self.windDir = rawData["windDirection"]
        