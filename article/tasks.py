import logging
import asyncio
from datetime import datetime

from django.utils import timezone

from .channel.newsapi.handlers import async_get_article_pages
from .channel.article import ArticlePage
from .auditors import check_article_title_for_bad_words
from .repository import article_record_abulk_update
from .rewrite.chatgpt.handlers import rewrite_articles_for_kids


_log = logging.getLogger(__name__)


async def save_rewrite_save(article_page: ArticlePage):
    _log.debug(f"Save rewrite save function started for article page number: {article_page.page_number}")

    # save featched data
    article_objs = await article_page.abulk_create()

    _log.debug(
        f"Article objects created: {len(article_objs)}" +
        f"for article page number: {article_page.page_number}"
    )

    # audit for words
    article_objs = check_article_title_for_bad_words(article_objs)

    # rewrite contents
    article_objs = await rewrite_articles_for_kids(article_objs)
    
    # save contents
    await article_record_abulk_update(article_objs)

    _log.debug(f"Objects processing finished for article page number: {article_page.page_number}")

    return len(article_objs)


async def async_featch_and_rewrite_news_articles(date_from, date_to):
    _log.debug(f"data fetching started from {date_from} to {date_to}")

    # fetch data from channel
    article_pages = await async_get_article_pages(date_from, date_to)

    _log.debug(f"Number of article pages fetched: {len(article_pages)}")

    coro_tasks = [
        save_rewrite_save(article_page)
        for article_page in article_pages
    ]
    results = await asyncio.gather(*coro_tasks)

    count = 0
    for r in results:
        count += r
    
    return count


def featch_and_rewrite_news_articles(date_from, date_to):
    # keep a single async event loop
    count = asyncio.run(async_featch_and_rewrite_news_articles(date_from, date_to))

    return count


def scheduled_featch_and_rewrite_news_articles(hours):
    date_from = timezone.now() - datetime(hour=hours)
    date_to = timezone.now()

    featch_and_rewrite_news_articles(date_from, date_to)
