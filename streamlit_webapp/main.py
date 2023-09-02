import streamlit as st
import pandas as pd
import time
import requests

st.title("Sensor readings and status")


def get_status_and_dataframe():
    res = requests.get("http://localhost:8000/data_and_predictions")
    if res.status_code == 200:
        table = pd.DataFrame(res.json()["data"])
        # print(table)
        # raise Exception(f"The table columns are {res.text}")
        table["reading_timestamp"] = pd.to_datetime(table["reading_timestamp"])
        status = res.json()["predictions"]
    else:
        table = pd.DataFrame(
            {
                "reading_timestamp": [],
                "moisture": [],
                "humidity": [],
                "temp_celsius": [],
            }
        )
        status = "None"

    return status, table


p1 = st.empty()
p2 = st.empty()
p3 = st.empty()
p4 = st.empty()
p5 = st.empty()
p6 = st.empty()

p7 = st.empty()
p8 = st.empty()
p9 = st.empty()

while True:
    status, table = get_status_and_dataframe()
    # p3.write
    p1.markdown("## Soil Moisture")
    p2.write(f"Status: {status['moisture']}")
    p3.line_chart(data=table, x="reading_timestamp", y="moisture")

    p4.markdown("## Humidity")
    p5.write(f"Status: {status['humidity']}")
    p6.line_chart(data=table, x="reading_timestamp", y="humidity")

    p7.markdown("## Temperature in Celsius")
    p7.write(f"Status: {status['temp_celsius']}")
    p9.line_chart(data=table, x="reading_timestamp", y="temp_celsius")
    time.sleep(30)
