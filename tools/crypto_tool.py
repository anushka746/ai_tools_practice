import requests
import os
import json


trusted_symbols = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "doge": "dogecoin",
    "sol": "solana",
    "xrp": "ripple",
    "ada": "cardano",
    "bnb": "binancecoin",
    "matic": "polygon",
    "ltc": "litecoin",
    "dot": "polkadot"
}


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

    
    name_map = {}


    for coin in coin_list:
        name = coin.get("name", "").lower()
        coin_id = coin.get("id")
        if name and coin_id:
            name_map[name] = coin_id

    return  name_map












name_map = build_symbol_map()


def crypto_tool(coin:str):
    try:
        if not coin or not coin.strip():
            return {"Error": "Coin Name is required"}
        
        coin = coin.strip().lower()
        if coin in trusted_symbols:
            coin_id = trusted_symbols [coin]

        # 2️⃣ Full coin name (bitcoin, ethereum, etc.)
        elif coin in name_map:
            coin_id = name_map[coin]
       
        url=f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_market_cap=true&include_24hr_change=true"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return {"Error": f"Failed to fetch data from API: {response.status_code}"}
        
        data = response.json()
        if coin_id not in data:
            return {"status": "ERROR",
                   
            "message":"Coin not found or is not supported",
            } 
        info=data[coin_id]
        return {
            "crypto": coin_id,
            "price_usd": info.get("usd"),
            "market_cap": info.get("usd_market_cap"),
            "change_24h": info.get("usd_24h_change")
        }
        
    except Exception as e:
        return {"status": "ERROR",
                "message":str(e)}

