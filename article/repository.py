import hashlib
import logging

from .channel.article import ArticlePage
from .models import ArticleRecord, NewsApiFetchLog, NewsSource


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
            id = hashlib.sha256(
                f"{article.title.lower()}:{article_page.source_id.lower()}".encode('utf-8')
            ).hexdigest()

            record_objs.append(
                ArticleRecord(
                    id=id,
                    source_id=article_page.source_id,
                    author=article.author,
                    published_at=article.published_at,
                    title=article.title,
                    description=article.description,
                    content=article.content,
                    url=article.url,
                    image_url=article.image_url,
                    channel_name=article_page.channel_name,
                    channel_response=article.response
                )
            )
        
        ArticleRecord.objects.abulk_create(record_objs, ignore_conflicts=True)
        total_record_objs += record_objs
    
    return total_record_objs


def create_modified_articles(article_records):
    ...


def get_news_api_fetch_log(source_id):
    ...



def create_newsapi_fetch_log(date_from, date_to, source_id) -> NewsApiFetchLog:
    return NewsApiFetchLog.objects.create(
        date_from=date_from,
        date_to=date_to,
        source_id=source_id
    )
