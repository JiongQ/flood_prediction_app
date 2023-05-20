APP_TITLE = 'Singapore Flood Prediction App'
APP_SUB_TITLE = 'Training Data Source: PUB and NEA'

selected_sensor_master_list = 'data/selected_sensor_master_list.csv'
weather_forecast_csv = 'data/weather_forecast.csv'
predicted_flood_risks = 'data/predicted_flood_risks.csv'
ml_trained_model = r'L://Data Cleaning//processing//ml_result__3_flood_risk/ada_boost/'
sg_postcode = r'data/sg_zipcode_mapper.csv'

df_postcode = None
df_sensor_master = None
user_address = 'NUS'

first_run = True