import streamlit as st
import folium
from streamlit_folium import st_folium
import sg_map as sg
import sensor
import pandas as pd
import config
import chatbot
import geopy.distance



def my_display_text_box():
    postal_code = st.sidebar.text_input('Postal Code',value='119077')
    return postal_code


def calculate_user_location(fg):
    fg = folium.FeatureGroup(name="Markers")
    fg.add_child(sensor.add_user_marker(st.session_state["myPostcode"]))


def load_data():
    config.df_postcode = pd.read_csv(config.sg_postcode, encoding = "latin-1")
    config.df_predicted_flood_risks_FINAL = pd.read_csv(config.predicted_flood_risks_FINAL).reset_index()
    config.df_emergency_station = pd.read_csv('data/emergency_orgs.csv')

def update_address(postcode):
    for index, row in config.df_postcode.iterrows():
        if row['postal'] == int(postcode):
            config.user_address = row['address']



def my_display_prediction(title, info):
    st.metric(title, info)


def get_nearest_E_location(postcode):
    for index, row in config.df_postcode.iterrows():
        if row['postal'] == int(postcode):
            user_lat = row['latitude']
            user_lon = row['longtitude']
            break

    coords_1 = (user_lat, user_lon)
    

    nearest_E_distance = 1000000
    nearest_E = None
    for index, row in config.df_emergency_station.iterrows():
        coords_2 = (row['Lattitude '], row['Longtitude '])
        distance = geopy.distance.geodesic(coords_1, coords_2).km

        if nearest_E is None:
            nearest_E = row['Emergency Organisation']

        if distance <= nearest_E_distance:
            nearest_E_distance = distance
            nearest_E = row['Emergency Organisation']

    return nearest_E, round(nearest_E_distance,3)
