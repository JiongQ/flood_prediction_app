import requests
import json
import pandas as pd
import config
import pickle
import os
from pathlib import Path
import numpy as np
# from sklearn import *


def call_weather_forecast_api():
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

    querystring = {"q":"Singapore","days":"3"}

    headers = {
        "X-RapidAPI-Key": "da0f72faf0mshcb8f071f62218fep1cd60cjsnc3946c24f5b4",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    # update_weather_forecast_csv(response.json())
    return response.json()


def get_weather_forecast():
    json_obj = call_weather_forecast_api()
    # print(type(json_obj))
    dict_days = json_obj['forecast']['forecastday']
    df_result = pd.DataFrame(columns=['time', 'precip_mm','will_it_rain', 'chance_of_rain'])
    # print(f'Length: {len(dict_days)}')

    for i in range(0,3):
        df_0 = pd.json_normalize(dict_days[i]['hour'])
        df_1 = df_0[['time', 'precip_mm', 'will_it_rain', 'chance_of_rain']].copy()
        df_result = pd.concat([df_result, df_1])        

    df_result.to_csv(config.weather_forecast_csv, index=False)
    # print('df_result Weather Forecast:')
    # print(df_result)
    return df_result


def update_predicted_flood_risk_csv():
    df_weather_forecast = get_weather_forecast()
    df = df_weather_forecast.reset_index()
    print(' => df_weather_forecast')
    print(df_weather_forecast)

    df_result = pd.DataFrame(columns=['time', 'sensor_id', 'flood_risk'])
    for index, row in df.iterrows():
        predicted_rainfall = row['will_it_rain'] * row['precip_mm'] * 60
        df0 = run_ml_models(predicted_rainfall, row['time'])
        # print('df0')
        # print(df0)
        df_result = pd.concat([df_result, df0])  
        
    df_result.to_csv(config.predicted_flood_risks, index=False)
    print('df_final_result')
    print(df_result)
        

def run_ml_models(predicted_rain_fall: float, time):
    df = pd.DataFrame(columns=['time', 'sensor_id', 'flood_risk'])

    for _i in os.listdir(config.ml_trained_model):
        if not (_i.endswith('.sav')):
            continue
        
        path = config.ml_trained_model + _i
        X = np.array([[predicted_rain_fall] * 30], dtype=np.float32)
        with open(path, 'rb') as f:
            loaded_model = pickle.load(f)

        flood_risk = loaded_model.predict(X)
        _list = [time, _i.split('.')[0], flood_risk[0]]
        df.loc[len(df)] = _list
        print(' => flood_risk by sensor')
        print(df)
        # break

    return df



# https://developers.onemap.sg/privateapi/commonsvc/revgeocode?location=1.3,103.8&token=0v9hsciobp1ifa5bgpkin21cs3&buffer=100&addressType=all
    

def call_one_map_api():
    password = 'AlamakNoTimeToDoProject99'
    token = r'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEwMzQzLCJ1c2VyX2lkIjoxMDM0MywiZW1haWwiOiJraWV3anlAZ21haWwuY29tIiwiZm9yZXZlciI6ZmFsc2UsImlzcyI6Imh0dHA6XC9cL29tMi5kZmUub25lbWFwLnNnXC9hcGlcL3YyXC91c2VyXC9zZXNzaW9uIiwiaWF0IjoxNjg0NTczNDc5LCJleHAiOjE2ODUwMDU0NzksIm5iZiI6MTY4NDU3MzQ3OSwianRpIjoiOWI1MWJiNTFkZWFiMmMxMGYyNjJmMzE3NzI3NDQ0MGMifQ.8nNEloAg1_q2HLtAaEYD6IEjCEGvd-1qNUTcazEh0LU'
    lat = 1.44568799
    lon = 103.800694
    url = f'https://developers.onemap.sg/privateapi/commonsvc/revgeocode?location={lat},{lon}&token={token}&buffer=500&addressType=all'

    response = requests.get(url)
    print(response.json())
    return response.json()


# def get_one_map_token():
#     {
#     url  : "https://developers.onemap.sg/privateapi/auth/post/getToken" 
#     data :  {
#                 "email": "youremail@onemap.sg", 
#                 "password": "yourpassword"
#             }
#     }


