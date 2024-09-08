from datetime import datetime

from .article import ArticlePage
from .enums import NewsChannels
from .newsapi.handlers import fetch_article_pages as newsapi_fetch_article_pages


def fetch_article_pages(
        date_from: datetime, date_to:datetime, countries: list, languages: list,
        channel=NewsChannels.NEWSAPI
    ) -> list[ArticlePage]:

    "Posibility to add multiple channels"
    if channel not in NewsChannels:
        raise ValueError(f"No such channel: {channel}")
    
    if channel == NewsChannels.NEWSAPI:
        for pages in newsapi_fetch_article_pages(date_from, date_to, countries, languages):
            if not pages:
                continue
            yield pages
