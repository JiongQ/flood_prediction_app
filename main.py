import sys
print(sys.executable)

import streamlit as st
import pandas as pd
import function as f
import config
import sg_map as sg
import api
import sensor

import pandas as pd
import folium
from streamlit_folium import st_folium
import chatbot


def main():

    st.set_page_config(config.APP_TITLE)
    st.title(config.APP_TITLE)
    st.caption(config.APP_SUB_TITLE)

    f.load_data()

    map = sg.create_map_with_sensor()
    config.map_default_view = map.get_bounds()


    fg = folium.FeatureGroup(name="Markers")
    postcode = f.my_display_text_box()

    if st.sidebar.button('Calculate Result'):
        f.update_address(postcode)        
        fg.add_child(sensor.add_user_marker(postcode))
        config.nearest_flood_risk_location = 'Meng Suan OD'
        config.distance_to_nearest_risk_location = '8537m'
        E, E1 = f.get_nearest_E_location(postcode)
        config.nearest_E = E
        config.nearest_E_distance =E1
    
    if st.sidebar.button('Reset View'):
        print('reset triggered')
        map.fit_bounds(config.map_default_view)
  

    st.write('Postcode Adress:')
    st.write(config.user_address)
    st.write('This address shown as purple icon in map below')

    st_folium(map, key="new", feature_group_to_add=fg, width=700, height=450)#scrollWheelZoom=False

    st.subheader(f'Flood Prediction at {postcode}')

    f.my_display_prediction('Risk of Flood', 'Low')

    col1, col2= st.columns(2)

    with col1:
        f.my_display_prediction('Nearest High Flood Risk Location', f'{config.nearest_flood_risk_location}')
    with col2:
        f.my_display_prediction('Distance to High Flood Risk Location', f'{config.distance_to_nearest_risk_location}') 
    

    f.my_display_prediction('Nearest Emergency Organisation:', f'{config.nearest_E}')


    if config.nearest_E_distance=='NIL':
        unit = ''
    else:
        unit = 'km'
    f.my_display_prediction('Distance to Nearest Emergency Organisation:', f'{config.nearest_E_distance}{unit}')


    chatbot.add_chatbot()


def main__update_data():
    api.update_predicted_flood_risk_csv2()
    sensor.get_predicted_flood_risk_FINAL()


if __name__ == "__main__":
    main()
    # main__update_data()

    # api.get_complete_prediction_input_csv()


