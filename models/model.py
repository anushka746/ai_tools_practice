import json
import os
from mistralai import Mistral
from mistralai.models import tool

from tools.weather_tool import weather_tool
from tools.crypto_tool import crypto_tool

tools = [
    {
        "type": "function",
        "function": {
            "name": "weather_tool",
            "description": "Get real-time weather info for a city using OpenWeather API",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name. Leave empty if not provided by user."}
                },
                "required": []
            },
        }
    },
    
    {
        "type":"function",
        "function":{
            "name":"crypto_tool",
            "description":"get real time price info about bitcoin using coingecko API",
            "parameters":{
                "type":"object",
                "properties":{
                    "coin":{"type":"string","description":"coin name. Leave empty if not provided by user."}
            },
            "required":[]
        },
             
            
        }
         
    }
]   





model = "mistral-large-latest"


def call_llm(user_input:str):
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is required. Please set it in your .env file.")


    client = Mistral(api_key=api_key)
    prompt = f"{user_input}"

    
    system_prompt="""You are an intent detection and tool selection engine.

Available tools:
- weather_tool: for weather queries (needs city name)
- crypto_tool: for cryptocurrency price queries (needs coin name)

Rules:
- If the user asks about weather, ALWAYS call weather_tool
- If the user asks about crypto/coin prices, ALWAYS call crypto_tool
- If a required parameter is missing from the user's query, set it to null or empty string
- Call the appropriate tool based on intent, even if parameters are incomplete
- Only skip tool calling if the query is completely unrelated to weather or crypto

Examples:
- "What's the weather?" → call weather_tool with city=""
- "Weather in Paris" → call weather_tool with city="Paris"
- "Bitcoin price" → call crypto_tool with coin="bitcoin"
- "Crypto price" → call crypto_tool with coin=""
"""

   


    chat_response = client.chat.complete(
    model = model,
    messages = [ 
        {
            "role":"system",
            "content":system_prompt
        },
        {
            "role": "user",
            "content": prompt,
        },
    ],
    tools=tools

)
   
    message=chat_response.choices[0].message
    print(message)
   
  

    
    if not hasattr(message, "tool_calls") or not message.tool_calls:
        return {
            "status": "NO_TOOL",
            "reason": "Missing information or unsupported query"
        }
    tool_call = message.tool_calls[0]
    try:   
        raw_args=(tool_call.function.arguments)
        args = json.loads(raw_args)
    except Exception:
        return {
            "status": "INVALID_ARGS",
            "tool_name": tool_call.function.name
        }
      
         
        
       
       
    return{
            "status": "TOOL_CALL",
            "tool_name":tool_call.function.name,
            "arguments":args,
            
            
        }
    