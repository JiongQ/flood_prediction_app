import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

import numpy as np
from folium import plugins
from folium.plugins import HeatMap
import sensor
import config as config



@st.cache_resource
def create_map_with_sensor():
    
    map = folium.Map(location=[1.372083,103.819839], zoom_start = 11.49) 	

    sensor.add_sensors_to_map(map)

    return map