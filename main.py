from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import csv
from io import StringIO

app = FastAPI()

# Habilitar CORS para GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción se recomienda especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URL pública del CSV
CSV_URL = "https://docs.google.com/spreadsheets/d/1cotJ7Goay6NluG2SfVCxx-rlfnDPdZB0_wO5ExIoG4s/gviz/tq?tqx=out:csv&sheet=Lecturas"

# Modelos de respuesta
class Lectura(BaseModel):
    timestamp: str
    valor: str

class SensorResponse(BaseModel):
    sensor: str
    datos: list[Lectura]

@app.get("/sensor/{sensor_id}", response_model=SensorResponse)
def get_sensor(sensor_id: str):
    try:
        response = requests.get(CSV_URL)
        response.raise_for_status()
        csv_data = response.text
        reader = csv.DictReader(StringIO(csv_data))

        datos = []
        for row in reader:
            if sensor_id in row:
                datos.append({
                    "timestamp": row["Timestamp"],
                    "valor": row[sensor_id]
                })

        return {"sensor": sensor_id, "datos": datos}

    except Exception as e:
        print("❌ Error:", str(e))
        return {"sensor": sensor_id, "datos": []}
