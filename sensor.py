import pandas as pd
import function as f
import config as config
import folium


def add_sensors_to_map(map):
    df = pd.read_csv(config.selected_sensor_master_list)
    df = df.reset_index()  # make sure indexes pair with number of rows

    for index, row in df.iterrows():
        folium.Marker(
        location=[row['lat'],row['lon']],
        popup=row['sensor_id'] + ': ' + row['site_name'],
        # icon=folium.Icon(icon="info-sign"),
        icon=folium.Icon(color="blue", icon="cloud"),
        # icon=folium.Icon(color="purple",icon="user", prefix='fa')
        ).add_to(map)


    folium.Marker(
        location=[1.302083,103.829839],
        popup='User Location',
        # icon=folium.Icon(icon="info-sign"),
        # icon=folium.Icon(color="red", icon="cloud"),
        icon=folium.Icon(color="purple",icon="user", prefix='fa')
        ).add_to(map)