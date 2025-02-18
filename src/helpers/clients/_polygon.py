import pytz

from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from urllib.parse import urlencode
import decouple
import requests


config = decouple.AutoConfig(' ')
POLYGON_API_KEY = config("POLYGON_API_KEY", default=None, cast=str)


def transform_polygon_result(result):
    unix_timestamp = result.get("t") / 1000.0
    utc_timestamp = datetime.fromtimestamp(unix_timestamp, pytz.timezone("UTC"))   # t ~ The Unix Msec timestamp
    # print(utc_timestamp)
    return {
        "volume": result["v"],
        "vwap": result["vw"],
        "open": result["o"],
        "close": result["c"],
        "high": result["h"],
        "low": result["l"],
        "time": utc_timestamp,  
        "no_of_transactions": result["n"]
    }
    

# @dataclass is a Python decorator from the dataclasses module that automatically generates special methods for a class, such as __init__, __repr__, __eq__, and others. It is used to simplify the creation of classes that primarily store data.
@dataclass
class PolygonAPIClient:
    ticker: str = "AAPL"
    multiplier: int = 1
    timespan: str = "day"
    from_date: str = "2025-01-10"
    to_date: str = "2025-01-10"
    api_key: str = ""
    adjusted: bool = True
    sort: Literal["asc", "desc"] = "asc"

    def get_api_keys(self):
        return self.api_key or POLYGON_API_KEY
        
    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.get_api_keys()}"
        }

    def get_params(self):
        return {
            "adjusted": self.adjusted,
            "sort": self.sort
        }

    def generate_url(self, pass_auth=False):
        path = f"/v2/aggs/ticker/{self.ticker}/range/{self.multiplier}/{self.timespan}/{self.from_date}/{self.to_date}"
        url = f"https://api.polygon.io{path}"
        params = self.get_params()
        encoded_params = urlencode(params)
        url = f"{url}?{encoded_params}"
        if pass_auth:
            url += f"&apikey={self.get_api_keys()}"
        return url

    def fetch_data(self):
        headers = self.get_headers()
        url = self.generate_url()
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # not for 200/201
        return response.json()

    def get_stock_data(self):
        data = self.fetch_data()
        results = data['results']
        return [transform_polygon_result(result) for result in results]
        # dataset = []
        # for result in results:
        #     dataset.append(
        #         transform_polygon_result(result)
        #     )
        # return dataset


"""
# Creating an instance
client = PolygonAPIClient()
print(client)  # Outputs: PolygonAPIClient(ticker='AAPL', multiplier=1, timespan='day', ...)
"""