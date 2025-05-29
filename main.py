from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import csv
import requests
from io import StringIO
from typing import List
from pydantic import BaseModel
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CSV_URL = os.environ.get("CSV_URL")

class DatoSensor(BaseModel):
    timestamp: str
    valor: str

class SensorResponse(BaseModel):
    sensor: str
    datos: List[DatoSensor]

@app.get("/lecturas")
def get_lecturas():
    response = requests.get(CSV_URL)
    if response.status_code != 200:
        return {"error": "No se pudo obtener el archivo CSV"}
    decoded = response.content.decode("utf-8")
    reader = csv.DictReader(StringIO(decoded))
    data = [row for row in reader]
    return {"lecturas": data}

@app.get("/sensor/{sensor_id}", response_model=SensorResponse)
def get_sensor(sensor_id: str):
    response = requests.get(CSV_URL)
    if response.status_code != 200:
        return {"sensor": sensor_id, "datos": []}
    decoded = response.content.decode("utf-8")
    reader = csv.DictReader(StringIO(decoded))
    datos = []
    for row in reader:
        if sensor_id in row:
            datos.append({
                "timestamp": row["Timestamp"],
                "valor": row[sensor_id]
            })
    return {"sensor": sensor_id, "datos": datos}
