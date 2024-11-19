from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()


class WeatherWarning(BaseModel):
    message: str


class WeatherResponse(BaseModel):
    temperature: float
    messages: list[WeatherWarning]


API_KEY = os.getenv("WEATHER_API_KEY")
if not API_KEY:
    raise Exception("API key not found. Please set it in the .env file.")
BASE_URL = 'http://api.weatherapi.com/v1/current.json'

@app.get("/weather/{zipcode}", response_model=WeatherResponse)
async def get_weather(zipcode: str):
    url = f"{BASE_URL}?key={API_KEY}&q={zipcode}&aqi=no"
    response = requests.get(url)
    
    if response.status_code == 200:
        weather_data = response.json()
        current_temp = weather_data['current']['temp_f']
        precipitation = weather_data['current']['precip_mm']
        
        messages = []
        
        if current_temp < 60 or current_temp > 75:
            messages.append(WeatherWarning(message="WARNING: Temperature NOT within 60-75°F range."))
        else:
            messages.append(WeatherWarning(message="Temperature is within safe range."))
        
        if precipitation > 0:
            messages.append(WeatherWarning(message="WARNING: There is precipitation."))
        else:
            messages.append(WeatherWarning(message="No precipitation detected."))
        
        return WeatherResponse(
            temperature=current_temp,
            messages=messages
        )
    
    else:
        raise HTTPException(status_code=500, detail="Error retrieving weather data")
