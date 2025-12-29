from tavily import TavilyClient
import requests
import os

# Get API key from environment variable
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY environment variable is required. Please set it in your .env file.")

tavily_client = TavilyClient(api_key=tavily_api_key)
response = tavily_client.search("latest ai news")

print(response)