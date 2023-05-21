import requests
import json
import pandas as pd
import config
import pickle
import os
from pathlib import Path
import numpy as np


def call_regional_weather_history_api(lat_lon):
    url = 'http://api.weatherapi.com/v1/history.json'
    # yyyy-MM-dd
    querystring = {"q":lat_lon,"dt":"2023-05-20", 'key': 'ce076abb141645769fb13448232105'}
    response = requests.get(url, params=querystring)
    # print(response.json())

    return response.json()


def get_raw_regional_history_rainfall(region):
    lat_lon = config.sg_region_lat_lon[region]
    json_obj = call_regional_weather_history_api(lat_lon)
    # print(json_obj)

    dict_days = json_obj['forecast']['forecastday']
    df_result = pd.DataFrame(columns=['time', 'precip_mm','will_it_rain', 'chance_of_rain'])

    df_0 = pd.json_normalize(dict_days[0]['hour'])
    df_1 = df_0[['time', 'precip_mm', 'will_it_rain', 'chance_of_rain']].copy()
    df_result = pd.concat([df_result, df_1])        

    # filename = config.weather_forecast_csv.split('.')[0]
    # df_result.to_csv(f'{filename}__History__{region}.csv' , index=False)
    return df_result


def get_processed_regional_history_rainfall(region):
    df = get_raw_regional_history_rainfall(region)
    df['predicted_rainfall'] = df['will_it_rain'] * df['precip_mm'] * 10#60
    df_result = df[['time', 'predicted_rainfall']]

    return df_result


def get_last_5_history_input_csv():
    df_E = get_processed_regional_history_rainfall('E')
    df_C = get_processed_regional_history_rainfall('C')
    df_N = get_processed_regional_history_rainfall('N')
    df_NE = get_processed_regional_history_rainfall('NE')
    df_W = get_processed_regional_history_rainfall('W')

    df = pd.DataFrame()
    df['Time'] = df_C['time']
    df['central'] = df_C['predicted_rainfall']
    df['east'] = df_E['predicted_rainfall']
    df['north-east'] = df_NE['predicted_rainfall']
    df['north'] = df_N['predicted_rainfall']
    df['west'] = df_W['predicted_rainfall']

    df_result = add_previous_hours_record(df)

    last_5_history = df_result.iloc[-5]
    last_5_history.to_csv(config.complete_lastday_history, index=False)
    # print(last_5_history)
    return last_5_history
    
#==============================================================


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


def call_regional_weather_forecast_api(lat_lon):
    url = 'http://api.weatherapi.com/v1/forecast.json'

    querystring = {"q":lat_lon,"days":"3", 'key': 'ce076abb141645769fb13448232105'}
    response = requests.get(url, params=querystring)
    return response.json()


def get_processed_regional_predicted_rainfall(region):
    df = get_raw_regional_predicted_rainfall(region)
    df['predicted_rainfall'] = df['will_it_rain'] * df['precip_mm'] * 10 #60
    df_result = df[['time', 'predicted_rainfall']]
    # print(df_result)
    return df_result


def get_raw_regional_predicted_rainfall(region):
    lat_lon = config.sg_region_lat_lon[region]
    json_obj = call_regional_weather_forecast_api(lat_lon)
    # print(json_obj)

    dict_days = json_obj['forecast']['forecastday']
    df_result = pd.DataFrame(columns=['time', 'precip_mm','will_it_rain', 'chance_of_rain'])
    # print(f'Length: {len(dict_days)}')

    for i in range(0,3):
        df_0 = pd.json_normalize(dict_days[i]['hour'])
        df_1 = df_0[['time', 'precip_mm', 'will_it_rain', 'chance_of_rain']].copy()
        df_result = pd.concat([df_result, df_1])        

    # filename = config.weather_forecast_csv.split('.')[0]
    # df_result.to_csv(f'{filename}__History__{region}.csv' , index=False)
    return df_result


def get_complete_prediction_input_csv():
    df_E = get_processed_regional_predicted_rainfall('E')
    df_C = get_processed_regional_predicted_rainfall('C')
    df_N = get_processed_regional_predicted_rainfall('N')
    df_NE = get_processed_regional_predicted_rainfall('NE')
    df_W = get_processed_regional_predicted_rainfall('W')

    df = pd.DataFrame()
    df['Time'] = df_C['time']
    df['central'] = df_C['predicted_rainfall']
    df['east'] = df_E['predicted_rainfall']
    df['north-east'] = df_NE['predicted_rainfall']
    df['north'] = df_N['predicted_rainfall']
    df['west'] = df_W['predicted_rainfall']
    
    df_0 = add_previous_hours_record(df)
    # last_5_history = get_last_5_history_input_csv()
    # lists = [last_5_history, df_0]
    # df_result = pd.concat(lists)

    df_0.to_csv(config.complete_prediction_input, index=False)
    return df_0
    # print(df_0)


def add_previous_hours_record(df):

    df['central_-1'] = df['central'].shift(1).ffill()
    df['east_-1'] = df['east'].shift(1).ffill()
    df['north-east_-1'] = df['north-east'].shift(1).ffill()
    df['north_-1'] = df['north'].shift(1).ffill()
    df['west_-1'] = df['west'].shift(1).ffill()

    df['central_-2'] = df['central'].shift(2).ffill()
    df['east_-2'] = df['east'].shift(2).ffill()
    df['north-east_-2'] = df['north-east'].shift(2).ffill()
    df['north_-2'] = df['north'].shift(2).ffill()
    df['west_-2'] = df['west'].shift(2).ffill()

    df['central_-3'] = df['central'].shift(3).ffill()
    df['east_-3'] = df['east'].shift(3).ffill()
    df['north-east_-3'] = df['north-east'].shift(3).ffill()
    df['north_-3'] = df['north'].shift(3).ffill()
    df['west_-3'] = df['west'].shift(3).ffill()

    df['central_-4'] = df['central'].shift(4).ffill()
    df['east_-4'] = df['east'].shift(4).ffill()
    df['north-east_-4'] = df['north-east'].shift(4).ffill()
    df['north_-4'] = df['north'].shift(4).ffill()
    df['west_-4'] = df['west'].shift(4).ffill()

    df['central_-5'] = df['central'].shift(5).ffill()
    df['east_-5'] = df['east'].shift(5).ffill()
    df['north-east_-5'] = df['north-east'].shift(5).ffill()
    df['north_-5'] = df['north'].shift(5).ffill()
    df['west_-5'] = df['west'].shift(5).ffill()

    df2 = df.iloc[5:]
    return df2
 

def get_weather_forecast():
    json_obj = call_weather_forecast_api()
    dict_days = json_obj['forecast']['forecastday']
    df_result = pd.DataFrame(columns=['time', 'precip_mm','will_it_rain', 'chance_of_rain'])

    for i in range(0,3):
        df_0 = pd.json_normalize(dict_days[i]['hour'])
        df_1 = df_0[['time', 'precip_mm', 'will_it_rain', 'chance_of_rain']].copy()
        df_result = pd.concat([df_result, df_1])        

    df_result.to_csv(config.weather_forecast_csv, index=False)
    # print('df_result Weather Forecast:')
    # print(df_result)
    return df_result


#==================================================================================


def update_predicted_flood_risk_csv2():
    # df_weather_forecast = get_weather_forecast()
    # df = df_weather_forecast.reset_index()

    df = get_complete_prediction_input_csv()
    print(df)
    df_feature = df.drop(['Time'], axis=1)
    time_list = df['Time'].to_list()

    df_result = pd.DataFrame(columns=['time', 'sensor_id', 'flood_risk'])
    for index, row in df_feature.iterrows():
        df0 = run_ml_prediction(row, time_list[index])
        df_result = pd.concat([df_result, df0])  
        
    df_result.to_csv(config.predicted_flood_risks, index=False)
    print('df_final_result')
    print(df_result)


def run_ml_prediction(_X, time):
    # df = get_complete_prediction_input_csv()
    df = pd.DataFrame(columns=['time', 'sensor_id', 'flood_risk'])
    X = _X.to_numpy().reshape(1, -1)
    print(X)

    for _i in os.listdir(config.ml_trained_model):
        if not (_i.endswith('.sav')):
            continue
        
        path = config.ml_trained_model + _i
        # X = np.array([[predicted_rain_fall] * 30], dtype=np.float32)
        with open(path, 'rb') as f:
            loaded_model = pickle.load(f)

        flood_risk = loaded_model.predict(X)
        _list = [time, _i.split('.')[0], flood_risk[0]]
        df.loc[len(df)] = _list
        print(' => flood_risk by sensor')
        print(df)

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


