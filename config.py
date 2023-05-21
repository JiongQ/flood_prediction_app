APP_TITLE = 'Singapore Flood Prediction App'
APP_SUB_TITLE = 'Training Data Source: PUB and NEA'

selected_sensor_master_list = 'data/selected_sensor_master_list.csv'
weather_forecast_csv = 'data/weather_forecast.csv'
predicted_flood_risks = 'data/predicted_flood_risks.csv'
predicted_flood_risks_FINAL = 'data/predicted_flood_risks_FINAL.csv'
ml_trained_model = r'L://Data Cleaning//processing//ml_result__3_flood_risk//_selected_models//'
sg_postcode = r'data/sg_zipcode_mapper.csv'


nearest_flood_risk_location = 'NIL'
distance_to_nearest_risk_location = 'NIL'
nearest_E = 'NIL'
nearest_E_distance = 'NIL'


df_postcode = None
df_predicted_flood_risks_FINAL = None
df_sensor_master = None
df_emergency_station = None
map_default_view = None


user_address = 'NUS'

first_run = True



# 529510	1.352527373	103.9446988	TAMPINES MALL
E_Region = '1.352527373,103.9446988'

# 39594	1.291573957	103.857027	MARINA MANDARIN
C_Region = '1.291573957,103.857027'

# 738099	1.436070059	103.7859815	CAUSEWAY POINT
N_Region = '1.436070059,103.7859815'

# 797653	1.391470154	103.8761255	THE SELETAR MALL
NE_Region = '1.391470154,103.8761255'

# 608549	1.333293345	103.7432787	JEM
W_Region = '1.333293345,103.7432787'


sg_region_lat_lon ={'E': E_Region,
                    'C': C_Region,
                    'N': N_Region,
                    'NE': NE_Region,
                    'W': W_Region}

complete_prediction_input = 'data/complete_prediction_input.csv'
complete_lastday_history = 'data/complete_lastday_history.csv'







