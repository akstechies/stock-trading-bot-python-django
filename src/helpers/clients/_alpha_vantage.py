import pytz

from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlencode
from decimal import Decimal
import requests
import decouple


config = decouple.AutoConfig(' ')
POLYGON_API_KEY = config("POLYGON_API_KEY", default=None, cast=str)
ALPHA_VANTAGE_API_KEY = config("ALPHA_VANTAGE_API_KEY", default=None, cast=str)


def transform_alphavantage_result(timestamp_str, result):
    timestamp_format = "%Y-%m-%d %H:%M:%S"
    eastern = pytz.timezone("US/Eastern")
    utc = pytz.utc
    
    timestamp = eastern.localize(datetime.strptime(timestamp_str, timestamp_format)).astimezone(utc)
    timestamp
    return {
        "volume": int(result["5. volume"]),
        "open": Decimal(result["1. open"]),
        "close": Decimal(result["4. close"]),
        "high": Decimal(result["2. high"]),
        "low": Decimal(result["3. low"]),
        "timestamp": timestamp,  
    }
    
@dataclass
class AlphaVantageAPIClient:
    ticker: str = "AAPL"
    function: str = "TIME_SERIES_INTRADAY"
    interval: str = "5min"
    api_key: str = ""
    month: str = "2024-12"

    def get_api_keys(self):
        return self.api_key or ALPHA_VANTAGE_API_KEY
        
    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.get_api_keys()}"
        }

    def get_params(self):
        return {
            "apikey": self.get_api_keys(),
            "function": self.function,
            "symbol": self.ticker,
            "interval": self.interval,
            "month": self.month
        }

    def generate_url(self):
        url = "https://www.alphavantage.co/query"
        params = self.get_params()
        encoded_params = urlencode(params)
        url = f"{url}?{encoded_params}"
        return url

    def fetch_data(self):
        headers = self.get_headers()
        url = self.generate_url()
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # not for 200/201
        return response.json()

    def get_stock_data(self):
        data = self.fetch_data()
        # print(data)
        dataset_key = [x for x in list(data.keys()) if not x.lower() == "meta data"][0]
        results = data[dataset_key]
        return [transform_alphavantage_result(timestamp, results.get(timestamp)) for timestamp in results.keys()]