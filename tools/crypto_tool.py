import requests
import os
import json

CACHE_FILE = "coin_list_cache.json"

def fetch_coin_list():
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()  #list of coins

def build_symbol_map():
    
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            coin_list = json.load(f)
    else:
        coin_list = fetch_coin_list()
        # Cache the result to avoid repeated calls
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(coin_list, f)

    symbol_map = {}
    for coin in coin_list:
        symbol = coin.get("symbol", "").lower()
        coin_id = coin.get("id")
        if symbol and coin_id:
            
            if symbol not in symbol_map:
                symbol_map[symbol] = coin_id
    return symbol_map


symbol_map = build_symbol_map()


def crypto_tool(coin:str):
    try:
        if not coin or not coin.strip():
            return {"Error": "Coin Name is required"}
        
        coin = coin.strip().lower()
        if coin in symbol_map:
            coin=symbol_map[coin]
        url=f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd&include_market_cap=true&include_24hr_change=true"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return {"Error": f"Failed to fetch data from API: {response.status_code}"}
        
        data = response.json()
        if coin not in data:
            return {"status": "ERROR",
                   
            "message":"Coin not found or is not supported",
            }
        info=data[coin]
        return {
            "crypto": coin,
            "price_usd": info.get("usd"),
            "market_cap": info.get("usd_market_cap"),
            "change_24h": info.get("usd_24h_change")
        }
        
    except Exception as e:
        return {"status": "ERROR",
                "message":str(e)}

