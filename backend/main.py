from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

from sqlalchemy import create_engine
import pandas as pd
import requests

app = FastAPI()
time.sleep(5)
# connection = connect(host="db", user="user", password="password", database="readings")
# cursor = connection.cursor()
engine = create_engine("mysql+pymysql://user:password@db:3306/readings")


@app.get("/data_and_predictions")
async def get_data():
    try:
        table = pd.read_sql_table("moistures", con=engine)

        last_row = table.sort_values("reading_timestamp", ascending=False).iloc[0]

        # print("my status")

        # print("my status_end")
        res = requests.post(
            "http://ml_service:8000/moisture",
            json={
                "timestamp": str(last_row["reading_timestamp"]),
                "moisture": str(last_row["moisture"]),
            },
        )
        # print(res.status_code)
        # print(res.text)
        status = res.json()["status"]
    except Exception as e:
        raise HTTPException(status_code=404, detail="Data not available yet")
    return {
        "data": table.to_dict("records"),
        "predictions": {"moisture": status},
    }
