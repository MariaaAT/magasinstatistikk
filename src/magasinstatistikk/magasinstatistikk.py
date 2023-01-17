import traceback
import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import streamlit as st
import mpld3
import streamlit.components.v1 as components

st.set_page_config(layout="wide")


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


def moving_average(data, time_frame=5):
    return data.rolling(time_frame).mean()


def filling_capacity(magasin, omrnr: int, year: str):
    df = pd.DataFrame(magasin, index=range(len(magasin)))  # DF created
    df['dato_Id'] = pd.to_datetime(df['dato_Id'])  # Convert dates into datetime dtype

    territory = df[df["omrnr"] == omrnr]
    territory = territory.sort_values("dato_Id")
    territory = territory[territory["dato_Id"] > year]

    territory_EL = territory[territory["omrType"] == "EL"]
    territory_EL["SMA5"] = moving_average(territory_EL['fyllingsgrad'])

    x1 = territory_EL["dato_Id"]
    y2 = territory_EL['fyllingsgrad']
    y4 = territory_EL['SMA5']

    fig, axs = plt.subplots()
    axs.plot(x1, y2, color='blue', label="Filling Capacity in EL Region")
    axs.plot(x1, y4, color='orange', label="SMA in EL Region")

    if omrnr in (1, 2, 3):  # VASS territory does not exist in regions 4 and 5
        territory_VASS = territory[territory["omrType"] == "VASS"]
        territory_VASS["SMA5"] = moving_average(territory_VASS['fyllingsgrad'])

        y1 = territory_VASS['fyllingsgrad']
        y3 = territory_VASS['SMA5']

        axs.plot(x1, y1, color='green', label="Filling Capacity in VASS Region")
        axs.plot(x1, y3, color='black', label="SMA in VASS Region")

    axs.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
    axs.xaxis.set_minor_locator(mdates.MonthLocator())
    axs.xaxis.set_major_formatter(mdates.ConciseDateFormatter(axs.xaxis.get_major_locator()))
    axs.set_xlabel('Date', fontsize=14)
    axs.set_ylabel(f'Lake Filling Capacity in Territory_{omrnr}', fontsize=14)
    plt.title(f"Lake Filling Capacity in {region_to_name(omrnr)} Norway since {year}", fontsize=15)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1), ncol=4)
    plt.gcf().set_size_inches(10, 5)
    axs.grid(True, linestyle='dotted')
    axs.margins(x=0)
    axs.set_ylim(0, 1.1)
    # plt.show()
    # st.pyplot(fig.figure)
    fig_html = mpld3.fig_to_html(fig)
    components.html(fig_html, height=800)


@st.cache
def load_magasin(url):
    parameters = {}
    response = requests.get(url, params=parameters)
    return json.loads(response.content)


omrnr = st.selectbox('Select a region', (1, 2, 3, 4, 5))

st.write('You selected region: ', f"{omrnr} - {region_to_name(omrnr)} Norway")

magasin = load_magasin("https://biapi.nve.no/magasinstatistikk/api/Magasinstatistikk/HentOffentligData")

try:
    filling_capacity(magasin, omrnr, "2015")
except:
    print(traceback.format_exc())
