import pytz
from datetime import datetime
import requests
import logging

from django.conf import settings
from .exceptions import NewsApiClientError


_log = logging.getLogger(__name__)


class NewsApiClient:

    def __init__(self, lang=['en']):
        self.lang = lang
        self.api_key = settings.TNA_API_KEY
    
    def _send_request(self, url: str, params: dict):
        if not self.api_key:
            raise NewsApiClientError("Set TNA_API_KEY in settings")
        
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
            
        except Exception as exc:
            raise NewsApiClientError(f"Could not request everything: {str(exc)}") from exc
        
        return response

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

        response = self._send_request(url, params)
        data = response.json()

        if not 'articles' in data:
            raise NewsApiClientError(
                f'Articles not in response data for url: {response.request.url}',
                status_code=response.status_code,
                response_text=response.text
            )
        
        if not data.get('articles'):
            _log.warning(f'No article found for url: {response.request.url}. params: {params}')

        return data
    
    def get_sources(self, countries: list[str]):
        url = 'https://newsapi.org/v2/top-headlines/sources'
        params = {
            'language': ','.join(self.lang),
            'country': ','.join(countries)
        }

        response = self._send_request(url, params)
        data = response.json()

        if not 'sources' in data:
            raise NewsApiClientError(
                f'Sources not in response data for url: {response.request.url}. params: {params}',
                status_code=response.status_code,
                response_text=response.text
            )

        if not data.get('sources'):
            _log.warning(f'No sources found for url: {response.request.url}')
        
        return data
        
