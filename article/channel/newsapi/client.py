import pytz
from datetime import datetime

from django.conf import settings
import aiohttp

from .exceptions import NewsApiClientError


class NewsApiClient:

    def __init__(self, lang=['en']):
        self.lang = lang

    async def aget_everything(
            self, from_param: datetime, to: datetime, page_size: int=100, page: int=1,
        ) -> dict:

        if page_size > 100:
            raise NewsApiClientError(
                f'everything endpoint has max 100 page size. value got: {page_size}'
            )
        
        if not settings.TNA_API_KEY:
            raise NewsApiClientError('missing TNA_API_KEY in settings')

        url = 'https://newsapi.org/v2/everything'
        headers = {
            'X-Api-Key': settings.TNA_API_KEY,
            'Content-Type': 'application/json'
        }
        params = {
            'from': from_param.astimezone(pytz.utc).isoformat(),
            'to': to.astimezone(pytz.utc).isoformat(),
            'language': ','.join(self.lang),
            'pageSize': page_size,
            'page': page,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status != 200:
                        raise NewsApiClientError(
                            f"Failed to fetch data, status code: {response.status}"
                        )
                    data = await response.json()
        except Exception as exc:
            raise NewsApiClientError(f"Could not request everything: {str(exc)}")
        
        return data
