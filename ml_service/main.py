from fastapi import FastAPI
from pydantic import BaseModel
from dateutil import parser
from mysql.connector import connect, Error


class Item(BaseModel):
    timestamp: str
    moisture: int


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Health Check"}


connection = connect(host="db", user="user", password="password", database="readings")
cursor = connection.cursor()


@app.post("/moisture/")
async def moisture(reading: Item):
    if reading.moisture < 1365:
        status = "high"
    elif reading.moisture < 2730:
        status = "optimum"
    else:
        status = "low"
    return {"status": status}
