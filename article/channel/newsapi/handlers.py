import logging
from datetime import datetime
import traceback
from typing import Generator

import pytz
from django.conf import settings
from django.utils import timezone

from article.repository import create_newschannel_fetch_log, get_or_create_news_source
from ..article import ArticlePage, Article
from .client import NewsApiClient
from ..utils import get_unfetched_time_ranges
from ..enums import NewsChannels


_log = logging.getLogger(__name__)


def parse_article_page_from_newsapi_response(response: dict, page: int, source_id: str) -> ArticlePage:
    articles = [
        Article(
            author=ra['author'],
            published_at=timezone.make_aware(
                datetime.strptime(ra['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"),
                pytz.utc
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
        channel=NewsChannels.NEWSAPI.value,
        articles=articles,
        source_id=source_id
    )

    return article_page


def fetch_source_article_page(date_from, date_to, source_id, languages) -> Generator[ArticlePage, None, None]:
    news_client = NewsApiClient(lang=languages)

    # Create page for first response
    response = news_client.get_everything(date_from, date_to, source_id, page=1)
    article_page = parse_article_page_from_newsapi_response(response, 1, source_id)
    yield article_page

    # create respone for other responses
    total_results = response['totalResults']
    if total_results > settings.TNA_PAGE_SIZE:
        range_end = total_results // settings.TNA_PAGE_SIZE + 1
        range_end = range_end + 1 if total_results % settings.TNA_PAGE_SIZE else range_end

        for page in range(2, range_end):
            response = news_client.get_everything(date_from, date_to, source_id, page=page)
            article_page = parse_article_page_from_newsapi_response(response, page, source_id)
            yield article_page



def fetch_article_pages(
        date_from: datetime, date_to: datetime, countries: list, languages: list
    ) -> list[ArticlePage]:
    news_client = NewsApiClient(lang=languages)
    source_response_data = news_client.get_sources(countries)

    sources_ids = [s['id'] for s in source_response_data['sources']]
    _log.info(
        f'Newsapi fetch starting for: countries: {countries}, languages: {languages},  sources: {sources_ids}'
    )

    # check article for each source
    for source_data in source_response_data['sources']:
        source_id = get_or_create_news_source(**source_data).id
        _log.info(f'Featiching for source: {source_id}')

        source_pages = []

        # create a unfetched time range
        unfetched_time_ranges = get_unfetched_time_ranges(date_from, date_to, NewsChannels.NEWSAPI.value, source_id)
        if not unfetched_time_ranges:
            _log.info(f'Fetched news api data before. date_from:{date_from} date_to:{date_to}, source: {source_id}')
            return
        
        # fetch article pages for that time range
        for udf, udt in unfetched_time_ranges:
            _log.info(f'Feching news api data for date_from:{udf} date_to:{udt}, source:{source_id}')

            fetch_log = create_newschannel_fetch_log(
                date_from=udf,
                date_to=udt,
                channel_name=NewsChannels.NEWSAPI.value,
                source_id=source_id,
            )

            try:
                for page in fetch_source_article_page(udf, udt, source_id, languages):
                    page.fetch_log_id = fetch_log.id
                    source_pages.append(page)
            
            except Exception as exc:
                _log.exception(exc)
                fetch_log.exception = traceback.format_exc()
            else:
                fetch_log.success = True
            finally:
                fetch_log.save()
        
        _log.info(f'Feching news api data complete for source: {source_id}')

        yield source_pages
    