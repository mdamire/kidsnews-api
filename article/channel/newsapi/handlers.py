import logging
from datetime import datetime
import asyncio

from django.conf import settings
from django.utils import timezone

from .client import NewsApiClient
from ..article import ArticlePage, Article


log = logging.getLogger(__name__)
news_client = NewsApiClient()


def parse_article_page_from_newsapi_response(response, page) -> ArticlePage:
    articles = [
        Article(
            author=ra['author'],
            published_at=timezone.make_aware(
                datetime.strptime(ra['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"),
                timezone.utc
            ),
            title=ra['title'],
            content=ra['content'],
            response=ra,
            description=ra['description'],
            url=ra['url'],
            image_url=ra['urlToImage']
        )
        for ra in response['articles']
    ]
    
    article_page = ArticlePage(
        page_number=page,
        channel='news-api',
        articles=articles
    )

    return article_page


async def fetch_newsapi_article_page(date_from, date_to, page) -> ArticlePage:
    response = await news_client.aget_everything(date_from, date_to, page=page)

    # parse in non-blocking way
    event_loop = asyncio.get_event_loop()
    articale_page = await event_loop.run_in_executor(
        None, 
        parse_article_page_from_newsapi_response,
        response
    )

    if page == 1:
        return (response['totalResults'], articale_page)
    
    return articale_page


async def async_get_article_pages(date_from, date_to) -> list[ArticlePage]:
    total_results, article_page_1 = await fetch_newsapi_article_page(
        date_from, 
        date_to, 
        1
    )

    tasks = [
        fetch_newsapi_article_page(date_from, date_to, page)
        for page in range(2, (total_results // settings.TNA_PAGE_SIZE) + 2)
    ]

    article_pages = await asyncio.gather(*tasks)

    return [article_page_1] + article_pages
