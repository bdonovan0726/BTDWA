import requests


class NOAAClient:
    BASE_URL = "https://api.weather.gov"

    def __init__(self):
        self.headers = {
            "User-Agent": "ocean-weather-app (you@example.com)",
            "Accept": "application/geo+json"
        }

    def get_point_metadata(self, lat: float, lon: float) -> dict:
        """Get forecast endpoints for a lat/lon"""
        url = f"{self.BASE_URL}/points/{lat},{lon}"
        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_hourly_forecast(self, lat: float, lon: float) -> dict:
        """Get hourly forecast (wind, temp, etc.)"""
        point_data = self.get_point_metadata(lat, lon)
        hourly_url = point_data["properties"]["forecastHourly"]

        resp = requests.get(hourly_url, headers=self.headers, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_latest_observation(self, station_id: str) -> dict:
        """Get latest observation from a NOAA station (wind, temp)"""
        url = f"{self.BASE_URL}/stations/{station_id}/observations/latest"
        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.raise_for_status()
        return resp.json()