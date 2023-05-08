import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# import json
import numpy as np
from folium import plugins
from folium.plugins import HeatMap
import sensor
import config as config


def _display_map(df, year, quarter):
    df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]

    map = folium.Map(location=[38, -96.5], zoom_start=4, scrollWheelZoom=False, tiles='CartoDB positron')
    
    choropleth = folium.Choropleth(
        geo_data='data/us-state-boundaries.geojson',
        data=df,
        columns=('State Name', 'State Total Reports Quarter'),
        key_on='feature.properties.name',
        line_opacity=0.8,
        highlight=True
    )
    choropleth.geojson.add_to(map)

    df_indexed = df.set_index('State Name')
    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['name']
        feature['properties']['population'] = 'Population: ' + '{:,}'.format(df_indexed.loc[state_name, 'State Pop'][0]) if state_name in list(df_indexed.index) else ''
        feature['properties']['per_100k'] = 'Reports/100K Population: ' + str(round(df_indexed.loc[state_name, 'Reports per 100K-F&O together'][0])) if state_name in list(df_indexed.index) else ''

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name', 'population', 'per_100k'], labels=False)
    )
    
    st_map = st_folium(map, width=700, height=450)

    state_name = ''
    if st_map['last_active_drawing']:
        state_name = st_map['last_active_drawing']['properties']['name']
    return state_name


def display_map():
    
    # m = folium.Map(location=[41,29],tiles="Stamen Toner",width="%100",height="%100")
    # folium.CircleMarker(location=(41,29),radius=100, fill_color='red').add_to(m)

    map = folium.Map(location=[1.372083,103.819839],zoom_start = 11.49)#  	

    # Add boundary line
    # f = open('./data/planning-boundary-area.json')
    # geojson = json.load(f)

    # folium.GeoJson(geojson, name="geojson").add_to(map)


    sensor.add_sensors_to_map(map)
   
    # HeatMap(data).add_to(folium.FeatureGroup(name='Heat Map').add_to(map))
    # folium.LayerControl().add_to(map)

    # folium.Circle(
    #     radius=100,
    #     location=[1.352083,103.929839],
    #     popup="The Waterfront",
    #     color="crimson",
    #     fill=False,
    # ).add_to(map)

    # folium.CircleMarker(
    #     location=[1.352083,103.859839],
    #     radius=50,
    #     popup="Laurelhurst Park",
    #     color="crimson",
    #     fill=True,
    #     fill_color="red",
    # ).add_to(map)



    # folium.Marker(
    #     location=[1.302083,103.829839],
    #     popup="City Hall",
    #     icon=folium.Icon(icon="cloud"),
    #     ).add_to(map)

    # folium.Marker(
    #     location=[1.352083,103.819839],
    #     popup="Bugis",
    #     icon=folium.Icon(color="green"),
    # ).add_to(map)

    # folium.Marker(
    #     location=[1.382083,103.809839],
    #     popup="AAA",
    #     icon=folium.Icon(color="red", icon="info-sign"),
    # ).add_to(map)

    st_map = st_folium(map, width=700, height=450)
