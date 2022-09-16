from turtle import onclick
import streamlit as st 
import pandas as pd 
import numpy as np 
import requests
import datetime
import plotly.figure_factory as ff
import plotly.express as px



# Custom imports 
from config.config import settings, time_format
from utils import utils 

# Page config 
st.set_page_config(
    page_title="Home IoT Dashboard",
    page_icon="📊",
    layout="wide",
    )

# Globals
global latest_data
global all_data
global date_range_specified_data
global start_date
global end_date
start_date = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days = 7), time_format)
end_date = datetime.datetime.strftime(datetime.datetime.now(), time_format)

latest_data = None
all_data = None
date_data = None 

def refresh_data():
    globals()['latest_data'] = utils.get_readings(url = f'{settings.api_base_url}/temperature/read/latest/', body = None)
    globals()['all_data'] = utils.get_readings(url = f'{settings.api_base_url}/temperature/read/all/', body = None)
    globals()['date_data'] = utils.get_readings(url = f'{settings.api_base_url}/temperature/read/date/', body = {
        'start_date': start_date,
        'end_date': end_date
    })

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == settings.streamlit_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        # Get latest data
        refresh_data()
        return True

if check_password():
    st.title("ESP32 - Temperature & Humidity")

    with st.sidebar:
        st.write("Filters & Refresh")

        # TODO: Add date filter

        dates = st.date_input(
            label = 'Select start and end date',
            value = (datetime.datetime.strptime(start_date, time_format), datetime.datetime.strptime(end_date, time_format)),
            )

        start_date = dates[0].strftime(time_format)
        try:
            end_date = dates[1].strftime(time_format)
        except: 
            pass 


        st.button(
            'Refresh data',
            key = None,
            help = 'Updates data',
            on_click = refresh_data()
            )

    all_data_df = pd.DataFrame.from_records(all_data).sort_values(by = ['dateTimeUtc'])
    date_data_df = pd.DataFrame.from_records(date_data).sort_values(by = ['dateTimeUtc'])

    st.metric(value = str(datetime.datetime.strptime(str(latest_data['dateTimeUtc']), time_format)),label ="Latest reading")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(value = str(round(latest_data['temperatureCelsius'], 2)) +  " C", label ="Current temperature")

        # Temperature filtered on date
        temperature_fig = px.line(date_data_df, x = 'dateTimeUtc', y = 'temperatureCelsius', title = '🌡️ Temperature, date filtered')
        temperature_fig.add_hline(
            y = date_data_df['temperatureCelsius'].mean(),
            line_color = 'Red'
        )

        st.plotly_chart(temperature_fig, use_container_width=True)

        # Temperature timeline 
        temperature_fig_all = px.line(all_data_df, x = 'dateTimeUtc', y = 'temperatureCelsius', title = '🌡️ Temperature')
        temperature_fig_all.add_hline(
            y = date_data_df['temperatureCelsius'].mean(),
            line_color = 'Red'
        )
        st.plotly_chart(temperature_fig_all, use_container_width=True)

    with col2:
        st.metric(value = str(round(latest_data['humidityPercentage'], 2)) + "%", label ="Current humidity")

        # Humidity filtered on date
        humidity_fig = px.line(date_data_df, x = 'dateTimeUtc', y = 'humidityPercentage', title = '💦 Humidity, date filtered')

        humidity_fig.add_hline(
            y = date_data_df['humidityPercentage'].mean(),
            line_color = 'Red'
        )

        st.plotly_chart(humidity_fig, use_container_width=True)

        # Humidity timeline 
        humidity_all_fig = px.line(all_data_df, x = 'dateTimeUtc', y = 'humidityPercentage', title = '💦 Humidity')
        humidity_all_fig.add_hline(
            y = date_data_df['humidityPercentage'].mean(),
            line_color = 'Red'
        )
        st.plotly_chart(humidity_all_fig, use_container_width=True)


    
