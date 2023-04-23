from typing import Union, Optional
import requests
import json
from datetime import date, datetime, timedelta
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import traceback

def region_to_name(omrnr: int) -> str:
    if omrnr == 1:
        return "Oslo / NO1 / Øst-Norge"
    if omrnr == 2:
        return "Kristiansand / NO2 / Sør-Norge"
    if omrnr == 3:
        return "Trondheim / NO3 / Midt-Norge"
    if omrnr == 4:
        return "Tromsø / NO4 / Nord-Norge"
    if omrnr == 5:
        return "Bergen / NO5 / Vest-Norge"
    return "UNKNOWN REGION"


def dmy(dt):
    day = dt.strftime('%d')
    month = dt.strftime('%m')
    year = dt.strftime('%Y')
    return day, month, year


def day_delta_to_name(day_delta: int) -> Optional[str]:
    if day_delta == 0:
        return "Today"
    if day_delta == 1:
        return "Tomorrow"
    return None

def price_plot(omrnr: int, day_delta: int = 0, mva: bool = False):
    dt = datetime.now()
    td = timedelta(days=day_delta)
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

    df["start"] = df['time_start'].dt.strftime('%H:%M')
    df["until"] = df['time_end'].dt.strftime('%H:%M')

    mva_factor = 1.25 if mva and omrnr != 4 else 1
    nettleie = 32.7
    df["ore_per_kWh"] = df['NOK_per_kWh'] * 100 * mva_factor + nettleie

    # Figure without taxes
    fig = go.Figure()


    y = round(df["ore_per_kWh"] , ndigits=2)
    max_price = round(df["ore_per_kWh"].max(), ndigits=2)

    fig.add_trace(go.Scatter(x=df["time_start"], y=y, name="", line=dict(shape='hv'), hovertemplate="%{y} Øre"))
    fig.update_yaxes(title=dict(text="Øre"), range=[0.1, max_price + 50])
    fig.update_xaxes(title=dict(text="Time"))

    fig.update_layout(title=dict(
        text=f"Electricity prices {'(inkludert avgifter og mva)' if mva else '(exkludert avgifter og mva)'}"),
                      hovermode="x unified", hoverlabel=dict(namelength=-1), showlegend=False, xaxis_tickformat='%H:%M')

    return df[["start", "until", "ore_per_kWh"]], fig


omrnr = st.selectbox('Select a region', (1, 2, 3, 4, 5), format_func=region_to_name)
day_delta = st.selectbox("Select a day", (0, 1), format_func=day_delta_to_name)
mva = st.checkbox('Inkludert avgifter og mva')

try:
    df, fig = price_plot(omrnr, day_delta, mva)
    st.write(fig)
    st.dataframe(df)
except:
    print(traceback.format_exc())