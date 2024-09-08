from datetime import datetime
import logging

from django.conf import settings

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


def process_daily_news_articles(
        date_from: datetime, date_to: datetime, 
        countries: list[str]=settings.NEWS_COUNTRIES, languages: list[str]=settings.NEWS_LANGUAGES
    ):
    _log.info(f"--- Starting article processing from {date_from} to {date_to} ---")

    task_results = []  # To store async task results

    for df, dt in utils.split_into_days(date_from, date_to):
        task = fetch_and_rewrite_news_articles.delay(df, dt, countries, languages)
        task_results.append(task)

    _log.info(f"--- Finished queuing article processing tasks from {date_from} to {date_to} ---")

    total_modified_records = 0
    for task in task_results:
        result = task.get()  
        total_modified_records += result

    _log.info(f"--- Total modified records: {total_modified_records} ---")

    return total_modified_records

