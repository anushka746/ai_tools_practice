# AI Weather & Crypto Tool

A web application that provides **current weather** information and **cryptocurrency prices**. Built with **HTML, CSS, JavaScript** on the frontend and **Python + FastAPI** on the backend. The app dynamically selects the appropriate tool based on user queries and handles errors gracefully.

## Features

- Get **weather information** for any city or your current location.
- Get **cryptocurrency prices** for popular coins (BTC, ETH, DOGE, etc.).
- Friendly and clear **error messages** for unsupported queries.
- Caches coin list from CoinGecko for faster queries.
- Clean and interactive **UI** with result cards for successful responses and simple messages for errors.

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python, FastAPI  
- **Dependencies:** `requests`, `fastapi`, `uvicorn`  
- **APIs Used:** CoinGecko API (crypto), OpenWeatherMap API (weather)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/anushka746/ai_tools_practice.git
cd ai_tools_practice  
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```


4. Create a .env file in the project root with your API keys:
```bash
MISTRAL_API_KEY=your_openai_key_here
WEATHER_API_KEY=your_weather_api_key_here
```

5. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

6. Open index.html in your browser to use the app.


## Usage

### Weather Queries

- **Full city name**  
  Example: `Weather in Mumbai`  
  Returns weather details including temperature, humidity, pressure, and descriptive labels.

- **No city provided**  
  The app will request **location permission** to fetch weather for your current location.

### Cryptocurrency Queries

- **Supported coins**  
  Use **coin symbols** (BTC, ETH, DOGE, etc.) or full coin names mapped internally.

- **Error handling**  
  Unsupported or unknown coins display a **clear, user-friendly message**.

### Examples
```text
- `Weather in New York`  
- `Current BTC price`  
- `Price of Ethereum`  
```

## Scope for Improvements

- Add **dynamic support for more cryptocurrencies** from CoinGecko.  
- Enhance UI with **charts or visual trends** for crypto prices and weather.  
- Support **multiple currencies** for cryptocurrency pricing.   
- Make the UI fully **responsive for mobile devices**.
