import uvicorn
from fastapi import FastAPI
import mlflow.sklearn
import pandas as pd
from pydantic import BaseModel

description = """
Bienvenue sur cette API! Nous allons faire une suggestion de prix de location à la journée grâce au Machiine learning.

Voici le endpoint: 
"""

tags_metadata = [
    {"name": "Introduction Endpoints",
     "description": "Endpoints de présentation"},
    {"name": "Prix de Location",
     "description": "Endpoints de tarification"}
]

app = FastAPI (
    title="API de Location de Voitures : Tarification",
    description=description,
    openapi_tags=tags_metadata
)

class Features(BaseModel):
    model_key: str
    mileage: int
    engine_power: int
    fuel : str
    paint_color: str
    car_type: str
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator	: bool
    winter_tires: bool

@app.get("/", tags=["Introduction Endpoints"])
async def index():
    message= "Bonjour tout le monde! Ceci `/` est le endpoint le plus simple de l'API. Si vous voulez en savoir plus, consultez la documentation de l' api ici: `/docs`"


@app.post("/predict", tags=["Prix de Location"])
async def predict(input_pred: Features):

    df = pd.DataFrame(dict(input_pred), index=[0])

    logged_model= "mlruns/419887017704619979/d69339d0070a4cc88b17a3f7f9f88d63/artifacts/price_car"

    loaded_model = mlflow.pyfunc.load_model(logged_model)

    prediction = loaded_model.predict(df)

    response = {"prediction": prediction.tolist()[0]}
    return response

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)