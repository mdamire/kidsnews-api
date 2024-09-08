from datetime import datetime, timedelta
import logging

from django.conf import settings
from django.utils import timezone

from kidsnews.celery import app
from .rewrite.handlers import rewrite_articles
from .repository import save_article_pages
from .channel.handlers import fetch_article_pages
from . import utils


_log = logging.getLogger(__name__)


@app.task
def fetch_and_rewrite_news_articles(
        date_from: datetime, date_to: datetime, countries: list[str], languages: list[str]
    ):
    modified_count = 0
    # loop through generator which yields list of ArticlePage for a single source of the country
    for article_pages in fetch_article_pages(date_from, date_to, countries, languages):
        if not article_pages:
            continue
        
        _log.info(f"Saving Article Pages")
        article_records = save_article_pages(article_pages)
        _log.info(f"article_records created: {len(article_records)}")

        _log.info("modifing article records")
        modified_records = rewrite_articles(article_records)
        _log.info(f"modified records created: {len(modified_records)}")

        modified_count += len(modified_records)
    
    return modified_count


def process_news_articles_by_time_period(
        date_from: datetime, date_to: datetime, 
        countries: list[str]=settings.NEWS_COUNTRIES, languages: list[str]=settings.NEWS_LANGUAGES
    ):
    """it will split up date into series of single days.
    meant to be called from management command
    """
    _log.info(f"--- Starting article processing from {date_from} to {date_to} ---")

    total_count = 0

    # Break down to 1 day period for better management
    for df, dt in utils.split_into_days(date_from, date_to):
        _log.info(f"Calling task: fetch_and_rewrite_news_articles. for {(df, dt, countries, languages)}")

        count = fetch_and_rewrite_news_articles(df, dt, countries, languages)
        total_count += count

        _log.info(f'Finished fetch_and_rewrite_news_articles for {(df, dt)}.  count: {count}')

    return total_count


@app.task
def process_latest_news_articles(hours):
    date_from = timezone.now() - timedelta(hours=hours)
    date_to = timezone.now()

    _log.info(f"--- Starting article processing from {date_from} to {date_to} ---")

    # break into hours for faster fetch
    for df, dt in utils.split_into_hours(date_from, date_to):
        _log.info(
            "Distributing task: fetch_and_rewrite_news_articles " +
            "for {( df, dt, settings.NEWS_COUNTRIES, settings.NEWS_LANGUAGES)}"
        )

        fetch_and_rewrite_news_articles.delay(
            df, dt, settings.NEWS_COUNTRIES, settings.NEWS_LANGUAGES
        )

    _log.info(f"--- Finished Distributing task fetch_and_rewrite_news_articles ---")

    return
