import requests


symbol_map = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "doge": "dogecoin",
    "sol": "solana",
    "xrp": "ripple",
}


def crypto_tool(coin:str):
    try:
        if not coin or not coin.strip():
            return {"Error": "Coin name is required"}
        
        coin = coin.strip().lower()
        if coin in symbol_map:
            coin=symbol_map[coin]
        url=f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd&include_market_cap=true&include_24hr_change=true"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return {"Error": f"Failed to fetch data from API: {response.status_code}"}
        
        data = response.json()
        if coin not in data:
            return {
            "Error":"Coin not found or is not supported",
            "supported_coins": list(symbol_map.keys())}
        info=data[coin]
        return {
            "crypto": coin,
            "price_usd": info.get("usd"),
            "market_cap": info.get("usd_market_cap"),
            "change_24h": info.get("usd_24h_change")
        }
        
    except Exception as e:
        return {"Error":str(e)}

