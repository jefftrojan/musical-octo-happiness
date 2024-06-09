import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uvicorn import Config, Server
import asyncio

# Load the trained model
model = joblib.load('potability.pkl')

app = FastAPI()

class WaterRequest(BaseModel):
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float

@app.get("/greet")
async def get_greet():
    return {"Message": "Hello"}

@app.get("/", status_code=status.HTTP_200_OK)
async def get_hello():
    return {"hello": "world"}

@app.post('/predict', status_code=status.HTTP_200_OK)
async def make_prediction(water_request: WaterRequest):
    try:
        single_row = [[
            water_request.ph,
            water_request.Hardness,
            water_request.Solids,
            water_request.Chloramines,
            water_request.Sulfate,
            water_request.Conductivity,
            water_request.Organic_carbon,
            water_request.Trihalomethanes,
            water_request.Turbidity]]
        predicted_portability = model.predict(single_row)
        return {"predicted_portability": predicted_portability[0][0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong.")
async def serve():
    config = Config(app)
    server = Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(serve())
    await server.serve()