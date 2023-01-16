import requests
import json
from datetime import date, datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import streamlit


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
    print(data)
    return data

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

    return data

todays_price(1)