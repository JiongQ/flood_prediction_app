import pandas as pd
import function as f
import config
import folium
import streamlit as st


def add_sensors_to_map(map):
    # df = df.reset_index()  # make sure indexes pair with number of rows

    for index, row in config.df_predicted_flood_risks_FINAL.iterrows():
        flood_string = ''

        if row['flood_risk'] == 'high':
            _color="red"
            _icon="info-sign"
            flood_string = '<br>' + 'Predicted Flood Time: <br>' + row['flood_time'].replace('|', '<br>')
        elif row['flood_risk'] == 'medium':
            _color="blue"
            _icon="cloud"
        else:
            _color="green"
            _icon="cloud"

        iframe = folium.IFrame(row['sensor_id'] + ': <br>' + row['site_name'] + flood_string)
        popup = folium.Popup(iframe, min_width=200, max_width=700)

        folium.Marker(
        location=[row['lat'],row['lon']],
        popup=popup,
   
        icon=folium.Icon(color=_color, icon=_icon),

        ).add_to(map)

    print('sensor rendered')


def get_predicted_flood_risk_FINAL():
    df_prediction = pd.read_csv(config.predicted_flood_risks)
    df_master = pd.read_csv(config.selected_sensor_master_list)
    df_master['flood_risk'] = 'low'
    df_master['flood_time'] = None

    print(df_prediction)
 
    for index, row in df_master.iterrows():
        _df =  df_prediction[(df_prediction.sensor_id == row['sensor_id']) &
                                    (df_prediction.flood_risk == 'high')]
        
        print('==============================')
        print(row['sensor_id'])
        print(len(_df))
        
        if len(_df) == 0:
            _df_medium =  df_prediction[(df_prediction.sensor_id == row['sensor_id']) &
                                        (df_prediction.flood_risk == 'medium')]
            print(f'medium length: {len(_df_medium)}')
        
            if len(_df_medium) > 0:
                print('write medium')
                df_master.at[index, 'flood_risk']= 'medium'
            continue

        else:
            df_master.at[index, 'flood_risk']= 'high'
            _df.sort_values(by='time', inplace = True)
            list = _df['time'].to_list()
            df_master.at[index, 'flood_time']= '|'.join(list)

    df_master.drop_duplicates(inplace=True)
    df_master.to_csv(config.predicted_flood_risks_FINAL, index=False)



def add_user_marker(postcode):
    print(postcode)
    got_data = False
    for index, row in config.df_postcode.iterrows():
        if row['postal'] == int(postcode):
            lat = row['latitude']
            lon = row['longtitude']
            config.user_address = row['address']
            got_data = True

    if not got_data:
        st.warning('Postcode entered in not found', icon="⚠️")
        return None

    return folium.Marker(       
        location=[lat, lon],
        popup='User Location',
        icon=folium.Icon(color="purple",icon="user", prefix='fa')
    )



