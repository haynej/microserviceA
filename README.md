# **Temperature and Precipitation Retrieval Microservice**


# Overview
This microservice will take a zip code as a parameter and return the temperature (in fahrenheit), a message indicating if the temperature is within the range of 60 to 75 degrees (a warning message if the temperature is not), and another message stating if there is precipitation or not for that location.

# Requirements
- FastAPI
- Flask
- Requests
- Uvicorn
- Pydantic
- python-dotenv (if the API key is in .env file instead of displayed in the app script)

# Requesting Data

The request script should include the requests dependency and should import it at the start of the script: 
import requests

The request should be made by a function that takes a zip code as a parameter.
This function should include:
- url variable: f"http://127.0.0.1:8000/weather/{zipcode}"   <-- if it is being hosted locally
- response variable that makes use of the requests dependency and gets the url variable
- a condition check to make sure the HTTP request was successful and returns 200:
    if the check is successful then the json response should be printed
    if the check fails then it should print an error or a status code

Example usage would be request_weather("90210")

# Receiving Data

As mentioned if the HTTP request is successful then it will send a json response from the weather API for the requested variables in the from of:
'temp_f'
'precip_mm'

The microservice will generate a list for messages and then will perform a conditional check for the temeprature and range and presence of precipitation.
Depending on the result of the conditional checks, messages will be appended to the messages list.
Finally, the microservice will return the WeatherResponse which includes a float for the temperature and messages variable containing the list of appended messages.

#UML Sequence Diagram

![image](https://github.com/user-attachments/assets/537e6825-b779-43de-92da-b79f276a2ddb)
