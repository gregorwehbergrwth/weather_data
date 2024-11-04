import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
	"latitude": 50.7766,
	"longitude": 6.0834,
	"start_date": "2024-10-28",
	"end_date": "2024-11-02",
	"hourly": ["temperature_2m", "relative_humidity_2m", "soil_temperature_0_to_7cm", "soil_temperature_7_to_28cm", "soil_temperature_28_to_100cm", "soil_temperature_100_to_255cm", "shortwave_radiation", "direct_radiation", "diffuse_radiation", "direct_normal_irradiance", "global_tilted_irradiance", "terrestrial_radiation"]
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_soil_temperature_0_to_7cm = hourly.Variables(2).ValuesAsNumpy()
hourly_soil_temperature_7_to_28cm = hourly.Variables(3).ValuesAsNumpy()
hourly_soil_temperature_28_to_100cm = hourly.Variables(4).ValuesAsNumpy()
hourly_soil_temperature_100_to_255cm = hourly.Variables(5).ValuesAsNumpy()
hourly_shortwave_radiation = hourly.Variables(6).ValuesAsNumpy()
hourly_direct_radiation = hourly.Variables(7).ValuesAsNumpy()
hourly_diffuse_radiation = hourly.Variables(8).ValuesAsNumpy()
hourly_direct_normal_irradiance = hourly.Variables(9).ValuesAsNumpy()
hourly_global_tilted_irradiance = hourly.Variables(10).ValuesAsNumpy()
hourly_terrestrial_radiation = hourly.Variables(11).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}
hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["soil_temperature_0_to_7cm"] = hourly_soil_temperature_0_to_7cm
hourly_data["soil_temperature_7_to_28cm"] = hourly_soil_temperature_7_to_28cm
hourly_data["soil_temperature_28_to_100cm"] = hourly_soil_temperature_28_to_100cm
hourly_data["soil_temperature_100_to_255cm"] = hourly_soil_temperature_100_to_255cm
hourly_data["shortwave_radiation"] = hourly_shortwave_radiation
hourly_data["direct_radiation"] = hourly_direct_radiation
hourly_data["diffuse_radiation"] = hourly_diffuse_radiation
hourly_data["direct_normal_irradiance"] = hourly_direct_normal_irradiance
hourly_data["global_tilted_irradiance"] = hourly_global_tilted_irradiance
hourly_data["terrestrial_radiation"] = hourly_terrestrial_radiation

hourly_dataframe = pd.DataFrame(data = hourly_data)
print(hourly_dataframe)

hourly_dataframe.to_csv(f'historical_data_{params["start_date"]}_{params["end_date"]}.csv', index=False)


