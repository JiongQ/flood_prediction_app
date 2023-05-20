import pandas as pd
import function as f
import config
import folium
import streamlit as st

# @st.cache_data
def add_sensors_to_map(map):
    # df = pd.read_csv(config.selected_sensor_master_list)
    # df = df.reset_index()  # make sure indexes pair with number of rows

    for index, row in config.df_sensor_master.iterrows():
        folium.Marker(
        location=[row['lat'],row['lon']],
        popup=row['sensor_id'] + ': ' + row['site_name'],
        # icon=folium.Icon(icon="info-sign"),
        icon=folium.Icon(color="blue", icon="cloud"),
        # icon=folium.Icon(color="purple",icon="user", prefix='fa')
        ).add_to(map)

    print('sensor rendered')


    # folium.Marker(
    #     location=[1.302083,103.829839],
    #     popup='User Location',
    #     # icon=folium.Icon(icon="info-sign"),
    #     # icon=folium.Icon(color="red", icon="cloud"),
    #     icon=folium.Icon(color="purple",icon="user", prefix='fa')
    #     ).add_to(map)


# def add_user_to_map(map, postcode):

#     for index, row in config.df_postcode.iterrows():
#         if row['postal'] == int(postcode):
#             lat = row['latitude']
#             lon = row['longtitude']

#     folium.Marker(       
#         location=[lat, lon],
#         popup='User Location',
#         # icon=folium.Icon(icon="info-sign"),
#         # icon=folium.Icon(color="red", icon="cloud"),
#         icon=folium.Icon(color="purple",icon="user", prefix='fa')
#     ).add_to(map)


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



