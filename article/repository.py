"""These are to intaract with database. 

Easy place to include additional actions with database actions.
"""
import hashlib
import logging
from typing import Generator

from django.db import transaction
from django.db.models import Q

from .channel.article import ArticlePage
from .models import ArticleRecord, NewsChannelFetchLog, NewsSource, ModifiedArticleRecord


_log = logging.getLogger(__name__)


def get_or_create_news_source(id, name, description, url, category, language, country) -> NewsSource:
    news_source, created = NewsSource.objects.get_or_create(
        id=id,
        defaults={
            'name': name,
            'description': description,
            'url': url,
            'category': category,
            'language': language,
            'country': country
        }
    )

    return news_source


def save_article_pages(article_pages: list[ArticlePage]):
    total_record_objs = []

    for article_page in article_pages:
        record_objs = []
        for article in article_page.articles:
            if article.title is None and article.content is None:
                continue

            # Create the id to pass around the object
            id = hashlib.sha256(
                f"{article.title.lower()}:{article_page.source_id.lower()}".encode('utf-8')
            ).hexdigest()

            record_objs.append(
                ArticleRecord(
                    id=id,
                    source_id=article_page.source_id,
                    author=article.author[:500] if article.author else None,
                    published_at=article.published_at,
                    title=article.title,
                    description=article.description,
                    content=article.content,
                    url=article.url,
                    image_url=article.image_url,
                    channel_name=article_page.channel_name[:64],
                    channel_response=article.response,
                    fetch_log_id=article_page.fetch_log_id
                )
            )
        
        try:
            ArticleRecord.objects.bulk_create(record_objs, ignore_conflicts=True)
            total_record_objs += record_objs
        except Exception as exc:
            try:
                NewsChannelFetchLog.objects.get(id=article_page.fetch_log_id).delete()
            except NewsChannelFetchLog.DoesNotExist:
                ...
            
            from django.forms.models import model_to_dict
            [_log.info(model_to_dict(record)) for record in record_objs]
            
            _log.exception(exc)
            continue
        
    
    return total_record_objs


def bulk_create_or_update_modified_records(records: list[ModifiedArticleRecord]):
    objs = []
    with transaction.atomic():
        objs = ModifiedArticleRecord.objects.bulk_create(
            records,
            update_conflicts=True,
            update_fields=['title', 'content', 'description'],
            unique_fields=['article'],
            batch_size=150
        )

    return objs


def create_newschannel_fetch_log(date_from, date_to, channel_name, source_id) -> NewsChannelFetchLog:
    return NewsChannelFetchLog.objects.create(
        date_from=date_from,
        date_to=date_to,
        channel_name=channel_name,
        source_id=source_id
    )


def get_articles_for_rewriting(date_from, date_to, chunk_size=100) -> list[ArticleRecord]:
    articles = ArticleRecord.objects.filter(
        published_at__gte=date_from,
        published_at__lte=date_to,
        modified_record__isnull=True,
        title_bad_words__isnull=True
    ).exclude(
        title_bad_words=''
    ).order_by('published_at')

    return articles
