import streamlit as st
import pandas as pd
import time
import requests

st.title("Sensor readings and status")
time.sleep(5)


def get_status_and_dataframe():
    res = requests.get("http://backend:8000/data_and_predictions")
    if res.status_code == 200:
        table = pd.DataFrame(res.json()["data"])
        # print(table)
        # raise Exception(f"The table columns are {res.text}")
        table["reading_timestamp"] = pd.to_datetime(table["reading_timestamp"])
        status = res.json()["predictions"]["moisture"]
    else:
        table = pd.DataFrame({"reading_timestamp": [], "moisture": []})
        status = "None"

    return status, table


p1 = st.empty()
p2 = st.empty()
# p3 = st.empty()


while True:
    status, table = get_status_and_dataframe()
    # p3.write
    p1.write(f"Status: f{status}")
    p2.line_chart(data=table, x="reading_timestamp", y="moisture")
    time.sleep(30)
