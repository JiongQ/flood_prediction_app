import sys
print(sys.executable)

import streamlit as st
import pandas as pd
import function as f
import config as config
import sg_map as sg


def main():

    st.set_page_config(config.APP_TITLE)
    st.title(config.APP_TITLE)
    st.caption(config.APP_SUB_TITLE)

    #Load Data
    df_continental = pd.read_csv('data/AxS-Continental_Full Data_data.csv')
    df_fraud = pd.read_csv('data/AxS-Fraud Box_Full Data_data.csv')
    df_median = pd.read_csv('data/AxS-Median Box_Full Data_data.csv')
    df_loss = pd.read_csv('data/AxS-Losses Box_Full Data_data.csv')

    #Display Filters and Map
    postcode = 732786
    postcode = f.my_display_text_box()
    # year, quarter = f.display_time_filters(df_continental)
    # state_name = f.display_map(df_continental, year, quarter)
    # state_name = f.display_state_filter(df_continental, state_name)
    sg.display_map()
    # state_name = 'Alabama'
    # report_type = f.display_report_type_filter()

    #Display Metrics
    # st.subheader(f'{state_name} {report_type} Facts')

    st.subheader(f'Flood Prediction at {postcode}')

    col1, col2, col3 = st.columns(3)

    # with col1:
    #     f.display_fraud_facts(df_fraud, year, quarter, report_type, state_name, 'State Fraud/Other Count', f'# of {report_type} Reports', string_format='{:,}')
    # with col2:
    #     f.display_fraud_facts(df_median, year, quarter, report_type, state_name, 'Overall Median Losses Qtr', 'Median $ Loss', is_median=True)
    # with col3:
    #     f.display_fraud_facts(df_loss, year, quarter, report_type, state_name, 'Total Losses', 'Total $ Loss')        

    with col1:
        f.my_display_prediction('Risk of Flood', 'Low')
    with col2:
        f.my_display_prediction('Nearest Emergency Center', '***')
    with col3:
        f.my_display_prediction('Other Info', '***') 

if __name__ == "__main__":
    main()