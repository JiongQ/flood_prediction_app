import streamlit as st
import folium
from streamlit_folium import st_folium
import sg_map as sg
import sensor
import pandas as pd
import config
import chatbot



def my_display_text_box():
    postal_code = st.sidebar.text_input('Postal Code',value='119077')
    return postal_code
    # return st.sidebar.text_input('Postal Code', value='732786', key="myPostcode", on_change=calculate_user_location(fg))


def calculate_user_location(fg):
    fg = folium.FeatureGroup(name="Markers")
    fg.add_child(sensor.add_user_marker(st.session_state["myPostcode"]))


def refresh_result():
    return st.sidebar.button('Calculate Result')


def update_address(postcode):
    for index, row in config.df_postcode.iterrows():
        if row['postal'] == int(postcode):
            config.user_address = row['address']



def my_display_prediction(title, info):
    st.metric(title, info)


def display_time_filters(df):
    year_list = list(df['Year'].unique())
    year_list.sort()
    year = st.sidebar.selectbox('Year', year_list, len(year_list)-1)
    # quarter = st.sidebar.radio('Quarter', [1, 2, 3, 4])
    quarter = st.sidebar.radio('Hello World', [1, 2, 3, 4])
    st.header(f'{year} Q{quarter}')
    return year, quarter

def display_state_filter(df, state_name):
    state_list = [''] + list(df['State Name'].unique())
    state_list.sort()
    state_index = state_list.index(state_name) if state_name and state_name in state_list else 0
    return st.sidebar.selectbox('State', state_list, state_index)

def display_report_type_filter():
    return st.sidebar.radio('Report Type', ['Fraud', 'Other'])

def display_map(df, year, quarter):
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

def display_fraud_facts(df, year, quarter, report_type, state_name, field, title, string_format='${:,}', is_median=False):
    df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]
    df = df[df['Report Type'] == report_type]
    if state_name:
        df = df[df['State Name'] == state_name]
    df.drop_duplicates(inplace=True)
    if is_median:
        total = df[field].sum() / len(df[field]) if len(df) else 0
    else:
        total = df[field].sum()
    st.metric(title, string_format.format(round(total)))

