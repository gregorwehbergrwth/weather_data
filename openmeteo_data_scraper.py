import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Define the parameters for the API request
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 50.7766,
    "longitude": 6.0834,
    "hourly": [
        "temperature_2m", "relative_humidity_2m", "soil_temperature_54cm",
        "shortwave_radiation", "direct_radiation", "diffuse_radiation",
        "direct_normal_irradiance", "global_tilted_irradiance", "terrestrial_radiation"
    ],
    "timezone": "Europe/Berlin",
    "forecast_days": 8,
    "models": ["icon_seamless", "icon_global", "icon_eu", "icon_d2"]
}
responses = openmeteo.weather_api(url, params=params)

# Initialize an empty DataFrame to store combined data from all models
combined_hourly_data = pd.DataFrame()

# Process data for each model
for i, response in enumerate(responses):
    model_name = response.Model()  # Get the name of the weather model
    print(model_name)
    print(params["models"][i])
    model_name = params["models"][i]
    # Create a dictionary to store the model-specific data
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(response.Hourly().Time(), unit="s", utc=True),
            end=pd.to_datetime(response.Hourly().TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=response.Hourly().Interval()),
            inclusive="left"
        )
    }
    # Fetch hourly variables, prefixing each key with the model name
    hourly_data[f"{model_name}_temperature_2m"] = response.Hourly().Variables(0).ValuesAsNumpy()
    hourly_data[f"{model_name}_relative_humidity_2m"] = response.Hourly().Variables(1).ValuesAsNumpy()
    hourly_data[f"{model_name}_soil_temperature_54cm"] = response.Hourly().Variables(2).ValuesAsNumpy()
    hourly_data[f"{model_name}_shortwave_radiation"] = response.Hourly().Variables(3).ValuesAsNumpy()
    hourly_data[f"{model_name}_direct_radiation"] = response.Hourly().Variables(4).ValuesAsNumpy()
    hourly_data[f"{model_name}_diffuse_radiation"] = response.Hourly().Variables(5).ValuesAsNumpy()
    hourly_data[f"{model_name}_direct_normal_irradiance"] = response.Hourly().Variables(6).ValuesAsNumpy()
    hourly_data[f"{model_name}_global_tilted_irradiance"] = response.Hourly().Variables(7).ValuesAsNumpy()
    hourly_data[f"{model_name}_terrestrial_radiation"] = response.Hourly().Variables(8).ValuesAsNumpy()

    # Convert the model-specific data to a DataFrame
    hourly_dataframe = pd.DataFrame(data=hourly_data)

    # Merge the data into the combined DataFrame
    if combined_hourly_data.empty:
        combined_hourly_data = hourly_dataframe
    else:
        combined_hourly_data = pd.merge(combined_hourly_data, hourly_dataframe, on="date", how="outer")

# Save the combined data to a CSV file
combined_hourly_data.to_csv('scraper_output_3.csv', index=False)