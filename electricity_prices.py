import requests
import json
from datetime import date, datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd


def region_to_name(omrnr: int) -> str:
    if omrnr == 1:
        return "Southeast"
    if omrnr == 2:
        return "Southwest"
    if omrnr == 3:
        return "Central"
    if omrnr == 4:
        return "Northern"
    if omrnr == 5:
        return "Western"
    return "UNKNOWN REGION"


def dmy(dt):
    day = dt.strftime('%d')
    month = dt.strftime('%m')
    year = dt.strftime('%Y')
    return day, month, year


def todays_price(omrnr: int):
    day, month, year = dmy(date.today())
    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{year}/{month}-{day}_NO{omrnr}.json"
    response = requests.get(url)
    data = json.loads(response.content)  # we can also use .text
    df = pd.DataFrame(data, index=range(len(data)))
    df['time_start'] = pd.to_datetime(df['time_start'])
    df['time_end'] = pd.to_datetime(df['time_end'])

    fig = go.Figure()
    y = df["NOK_per_kWh"] * 100
    fig.add_trace(go.Scatter(x=df["time_start"], y=y, name="", line=dict(shape='hv'), hovertemplate="%{y} Øre"))
    max_price = df["NOK_per_kWh"].max() * 100
    fig.update_yaxes(title=dict(text="Øre"), range=[0.1, max_price + 50])
    fig.update_xaxes(title=dict(text="Time"))
    fig.update_layout(title=dict(text=f"Electrocity prices"), hovermode="x unified", hoverlabel=dict(namelength=-1),
                      showlegend=False, xaxis_tickformat='%H')

    return fig


def tomorrows_prices(omrnr: int):
    dt = datetime.now()
    td = timedelta(days=1)
    my_date = dt + td
    day, month, year = dmy(my_date)
    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{year}/{month}-{day}_NO{omrnr}.json"

    try:
        response = requests.get(url)
        if not response.ok:
            return "Prices not available yet"
    except Exception as e:
        return f"Unknown error {e}"

    data = json.loads(response.content)  # we can also use .text
    df = pd.DataFrame(data, index=range(len(data)))
    df['time_start'] = pd.to_datetime(df['time_start'])
    df['time_end'] = pd.to_datetime(df['time_end'])

    fig = go.Figure()
    y = df["NOK_per_kWh"] * 100
    fig.add_trace(go.Scatter(x=df["time_start"], y=y, name="", line=dict(shape='hv'), hovertemplate="%{y} Øre"))
    max_price = df["NOK_per_kWh"].max() * 100
    fig.update_yaxes(title=dict(text="Øre"), range=[0.1, max_price + 50])
    fig.update_xaxes(title=dict(text="Time"))
    fig.update_layout(title=dict(text=f"Electrocity prices"), hovermode="x unified", hoverlabel=dict(namelength=-1),
                      showlegend=False, xaxis_tickformat='%H')
    return fig


