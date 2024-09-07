from .article import ArticlePage
from .enums import NewsChannels
from .newsapi.handlers import fetch_article_pages as newsapi_fetch_article_pages

def fetch_article_pages(date_from, date_to, countries, channel=NewsChannels.NEWSAPI) -> list[ArticlePage]:
    if channel == NewsChannels.NEWSAPI:
        for pages in newsapi_fetch_article_pages(date_from, date_to, countries):
            yield pages
    else:
        raise ValueError(f"No such channel: {channel}")
