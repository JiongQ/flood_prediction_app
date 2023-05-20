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

    # config.df_postcode = pd.read_csv(config.sg_postcode, encoding = "latin-1")
    # config.df_sensor_master = pd.read_csv(config.selected_sensor_master_list).reset_index()

    f.load_data()

    map = sg.create_map_with_sensor()
    config.map_default_view = map.get_bounds()

    # fg = folium.FeatureGroup(name="Markers")
    # fg.add_child(sensor.add_user_marker('119077'))
    # print('display sensors')
    fg = folium.FeatureGroup(name="Markers")
    postcode = f.my_display_text_box()

    # if f.refresh_result():
    if st.sidebar.button('Calculate Result'):
        f.update_address(postcode)        
        fg.add_child(sensor.add_user_marker(postcode))
    
    if st.sidebar.button('Reset View'):
        print('reset triggered')
        map.fit_bounds(config.map_default_view)
  

    st.write('Postcode Adress:')
    st.write(config.user_address)
    st.write('This address shown as purple icon in map below')

    st_folium(map, key="new", feature_group_to_add=fg, width=700, height=450)#scrollWheelZoom=False


        # map = sg.create_map_with_sensor()
        # rendered_map['zoom'] = 11.49
        # rendered_map['location'] = [1.372083,103.819839]


    st.subheader(f'Flood Prediction at {postcode}')

    col1, col2, col3 = st.columns(3)
  

    with col1:
        f.my_display_prediction('Risk of Flood', 'Low')
    with col2:
        f.my_display_prediction('Nearest Emergency Center', '***')
    with col3:
        f.my_display_prediction('Other Info', '***') 


    chatbot.add_chatbot()


def main__update_data():
    api.update_predicted_flood_risk_csv()


if __name__ == "__main__":
    main()
    # main__update_data()
    # api.call_one_map_api()