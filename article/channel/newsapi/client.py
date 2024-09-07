import pytz
from datetime import datetime
import requests

from django.conf import settings
from .exceptions import NewsApiClientError


class NewsApiClient:

    def __init__(self, api_key, lang=['en']):
        self.lang = lang
        self.api_key = api_key
    
    def _send_request(self, url: str, params: dict):
        headers = {
            'X-Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code != 200:
                raise NewsApiClientError(
                    "Failed to fetch data.",
                    status_code=response.status_code,
                    response_text=response.text
                )
            data = response.json()
        except Exception as exc:
            raise NewsApiClientError(f"Could not request everything: {str(exc)}") from exc
        
        return data

    def get_everything(
            self, from_param: datetime, to: datetime, source: str,
            page_size: int = 100, page: int = 1, 
        ) -> dict:

        if page_size > 100:
            raise NewsApiClientError(
                f'everything endpoint has max 100 page size. value got: {page_size}'
            )

        url = 'https://newsapi.org/v2/everything'
        params = {
            'from': from_param.astimezone(pytz.utc).isoformat(),
            'to': to.astimezone(pytz.utc).isoformat(),
            'language': ','.join(self.lang),
            'pageSize': page_size,
            'page': page,
            'sources': source
        }

        return self._send_request(url, params)
    
    def get_sources(self, countries: list[str]):
        url = 'https://newsapi.org/v2/everything'
        params = {
            'language': ','.join(self.lang),
            'country': ','.join(countries)
        }

        return self._send_request(url, params)
        
