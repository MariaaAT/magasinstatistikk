import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import requests
import json
import plotly.graph_objects as go
import traceback


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

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y2, mode="lines", name="Filling Capacity in EL Region"))
    fig.add_trace(go.Scatter(x=x1, y=y4, mode="lines", name="SMA in VASS Region"))

    # link for colours: https://community.plotly.com/t/plotly-colours-list/11730/3

    if omrnr in (1, 2, 3):  # VASS territory does not exist in regions 4 and 5
        territory_VASS = territory[territory["omrType"] == "VASS"]
        territory_VASS["SMA5"] = moving_average(territory_VASS['fyllingsgrad'])

        y1 = territory_VASS['fyllingsgrad']
        y3 = territory_VASS['SMA5']

        fig.add_trace(go.Scatter(x=x1, y=y1, mode="lines", name="Filling Capacity in VASS Region"))
        fig.add_trace(go.Scatter(x=x1, y=y3, mode="lines", name="SMA in VASS Region"))
        #newnames = {"fyllingsgrad": "Filling Capacity in VASS Region", "SMA5": "SMA in VASS Region", "x1": "Date"}
        #fig.for_each_trace(lambda t: t.update(name=newnames[t.name], legendgroup=newnames[t.name]))

    fig.update_layout(legend=dict(title=None, orientation="h", y=0.9, yanchor="bottom", x=0.5, xanchor="center"),
                      title=dict(text=f"Lake Filling Capacity in {region_to_name(omrnr)} Norway since {year}", y=1),
                      hovermode="x unified",
                      hoverlabel=dict(namelength=-1))
    fig.update_yaxes(title=dict(text=f'Lake Filling Capacity in Territory_{omrnr}'), range=[0, 1.2])
    fig.update_xaxes(title=dict(text="Date"))

    # fig.show() -> This opens a new tab on Google
    return fig

def load_magasin(url):
    parameters = {}
    response = requests.get(url, params=parameters)
    return json.loads(response.content)


omrnr = st.selectbox('Select a region', (1, 2, 3, 4, 5))

st.write('You selected region: ', f"{omrnr} - {region_to_name(omrnr)} Norway")

magasin = load_magasin("https://biapi.nve.no/magasinstatistikk/api/Magasinstatistikk/HentOffentligData")

try:
    st.write(filling_capacity(magasin, omrnr, "2015"))
except:
    print(traceback.format_exc())
