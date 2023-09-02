from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

from sqlalchemy import create_engine
import pandas as pd
import requests

app = FastAPI()

db_host = "localhost"
db_user = "user"
db_password = "password"
db_database = "readings"

engine = create_engine(
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_database}"
)


def get_moisture_status(reading: int) -> str:
    if reading > 90:
        status = "high"
    elif reading > 45:
        status = "optimum"
    else:
        status = "low"
    return status


def get_temp_status(reading: float) -> str:
    if reading > 40:
        status = "high"
    elif reading > 25:
        status = "optimum"
    else:
        status = "low"
    return status


def get_humidity_status(reading: int) -> str:
    if reading > 75:
        status = "high"
    elif reading > 35:
        status = "optimum"
    else:
        status = "low"
    return status


@app.get("/data_and_predictions")
async def get_data():
    try:
        table = pd.read_sql_table("moistures", con=engine)
        table["moisture"] = 100 - ((table["moisture"] / 4095) * 100)

        last_row = table.sort_values("reading_timestamp", ascending=False).iloc[0]
        moisture_status = get_moisture_status(last_row["moisture"])
        temp_status = get_temp_status(last_row["temp_celsius"])
        humidity_status = get_humidity_status(last_row["humidity"])
    except Exception as e:
        raise HTTPException(status_code=404, detail="Data not available yet")
    return {
        "data": table.to_dict("records"),
        "predictions": {
            "moisture": moisture_status,
            "temp_celsius": temp_status,
            "humidity": humidity_status,
        },
    }
