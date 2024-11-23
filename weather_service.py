from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()


class WeatherWarning(BaseModel):
    temp_message: str
    precip_message: str


class WeatherResponse(BaseModel):
    temperature: float
    messages: list[WeatherWarning]


API_KEY = os.getenv("WEATHER_API_KEY")
if not API_KEY:
    raise Exception("API key not found. Please set it in the .env file.")
BASE_URL = 'http://api.weatherapi.com/v1/current.json'


def evaluate_weather_conditions(temperature: float, precipitation: float) -> WeatherWarning:
    temp_message = (
        "WARNING: Temperature NOT within 60-75°F range."
        if temperature < 60 or temperature > 75
        else "Temperature is within safe range."
    )

    precip_message = (
        "WARNING: There is precipitation."
        if precipitation > 0
        else "No precipitation detected."
    )

    return WeatherWarning(temp_message=temp_message, precip_message=precip_message)


@app.get("/weather/{zipcode}", response_model=WeatherResponse)
async def get_weather(zipcode: str):
    url = f"{BASE_URL}?key={API_KEY}&q={zipcode}&aqi=no"
    response = requests.get(url)
    
    if response.status_code == 200:
        weather_data = response.json()
        current_temp = weather_data['current']['temp_f']
        precipitation = weather_data['current']['precip_mm']

        warning = evaluate_weather_conditions(current_temp, precipitation)

        return WeatherResponse(
            temperature=current_temp,
            messages=[warning]  # Wrap in a list to match the response model
        )
    
    else:
        raise HTTPException(status_code=500, detail="Error retrieving weather data")
