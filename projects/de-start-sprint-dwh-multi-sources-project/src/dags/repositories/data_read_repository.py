import requests
from typing import List
from logging import Logger


class DataReader:
    def __init__(self,
                 headers: dict,
                 url: str,
                 sort_field: str,
                 log: Logger) -> None:
        self.url = url
        self.headers = headers
        self.sort_field = sort_field
        self.sort_direction = "ASC"
        self.log = log

    def get_data(self, limit: str = None, offset: str = None) -> List:
        params = {
            "sort_field": self.sort_field,
            "sort_direction": self.sort_direction,
            "limit": limit,
            "offset": offset
        }
        response = requests.get(
            url=self.url,
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        json_data = response.json()
        # self.log.info(f"JSON {json_data}")

        if not isinstance(json_data, list):
            raise ValueError("Expected list in JSON response")

        return json_data

    def get_scd2_data(
            self, offset: str = None,
            from_ts: str = None, to_ts: str = None) -> List:
        params = {
            "sort_field": self.sort_field,
            "sort_direction": self.sort_direction,
            "offset": offset,
            "from": from_ts,
            "to": to_ts,
        }
        response = requests.get(
            url=self.url,
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        json_data = response.json()

        if not isinstance(json_data, list):
            raise ValueError("Expected list in JSON response")

        return json_data
