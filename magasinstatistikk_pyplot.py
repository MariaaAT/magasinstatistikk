import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import requests
import json

# Importing data
url = "https://biapi.nve.no/magasinstatistikk/api/Magasinstatistikk/HentOffentligData"
parameters = {}
response = requests.get(url, params=parameters)
magasin = json.loads(response.content)

# DF
df = pd.DataFrame(magasin, index=range(len(magasin)))
df['dato_Id'] = pd.to_datetime(df['dato_Id'])
territory_1 = df[df["omrnr"] == 1]
territory_1 = territory_1.sort_values("dato_Id")  # x values
territory_1_VASS = territory_1[territory_1["omrType"] == "VASS"]  # y values
x1 = territory_1_VASS["dato_Id"]
y1 = territory_1_VASS['fyllingsgrad']

# Line graph with plotly

fig = px.line(x=x1, y=y1)
fig.show()


