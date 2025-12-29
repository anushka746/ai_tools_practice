import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from models.model import call_llm
from tools.weather_tool import weather_tool
from tools.crypto_tool import crypto_tool



app = FastAPI()


allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://127.0.0.1:5500").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

class UserQuery(BaseModel):
    query: str
    latitude: Optional[float] = None 
    longitude: Optional[float] = None 

class LocationQuery(BaseModel):
    latitude: float
    longitude: float


@app.get('/')
async def root():
    return {"Message":"The app is running"}

@app.post("/query")
async def query_endpoint(user_query: UserQuery):
    llm_result= call_llm(user_query.query)
    status = llm_result["status"]

    
    if status == "NO_TOOL":
          return {
            "status": "NO_TOOL",
            "message": llm_result.get("message", "I can help only with weather and cryptocurrency prices.")
        }

    if status == "INVALID_ARGS":
        return {
            "status": "ERROR",
            "message": "Could not understand the request clearly."
        }

    if status != "TOOL_CALL":
        return {
            "status": "ERROR",
            "message": "Unexpected AI response."
        }

    
  
   
    tool_name = llm_result["tool_name"]
    args = llm_result["arguments"]

    
       
      
       
        
    if tool_name == "weather_tool":
        
        if "city" in args and args["city"]:
            result = weather_tool(city=args.get("city"), location=None)
            return {"status": "SUCCESS","result":result}
                
        elif user_query.latitude is not None and user_query.longitude is not None:
             result = weather_tool(
                city=None,
                location={
                    "lat": user_query.latitude,
                    "lon": user_query.longitude
                }
            )
             return {"status": "SUCCESS","result":result}
       
        else:
            return {
            "status": "NEED_LOCATION", 
            "message": "Please allow location access to get weather for your area, or specify a city name.",
            "tool": "weather_tool"
        }
    
    elif tool_name == "crypto_tool":
        if "coin" not in args or not args["coin"]:
            return {
                "status": "ERROR",
                "message": "Coin name is required for crypto queries."
            }
        result = crypto_tool(coin=args["coin"])
        return {"status": "SUCCESS","result": result}
    else:
        return {"status": "ERROR", "message": "Unsupported request."}


@app.post("/weather-by-location")
async def weather_by_location(location: LocationQuery):
    
    result = weather_tool(
        city=None,
        location={
            "lat": location.latitude,
            "lon": location.longitude
        }
    )
    print(result)
    return {"status": "SUCCESS", "result": result}