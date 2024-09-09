import uuid
import random
from datetime import datetime, timedelta
from django.utils import timezone
import factory

from article import models
from article.channel.article import Article, ArticlePage
from article.channel.enums import NewsChannels


def random_string(length=10):
    return ''.join(
        random.choices(
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 
            k=length
        )
    )


def newsapi_source_response(size=1):
    response = [
        {
            "id": "cbc-news",
            "name": "CBC News",
            "description": "CBC News is the division of the Canadian Broadcasting Corporation responsible for the news gathering and production of news programs on the corporation's English-language operations, namely CBC Television, CBC Radio, CBC News Network, and CBC.ca.",
            "url": "http://www.cbc.ca/news",
            "category": "general",
            "language": "en",
            "country": "ca"
        },
        {
            "id": "financial-post",
            "name": "Financial Post",
            "description": "Find the latest happenings in the Canadian Financial Sector and stay up to date with changing trends in Business Markets. Read trading and investing advice from professionals.",
            "url": "https://financialpost.com",
            "category": "business",
            "language": "en",
            "country": "ca"
        },
        {
            "id": "google-news-ca",
            "name": "Google News (Canada)",
            "description": "Comprehensive, up-to-date Canada news coverage, aggregated from sources all over the world by Google News.",
            "url": "https://news.google.com",
            "category": "general",
            "language": "en",
            "country": "ca"
        },
        {
            "id": "the-globe-and-mail",
            "name": "The Globe And Mail",
            "description": "The Globe and Mail offers the most authoritative news in Canada, featuring national and international news.",
            "url": "https://www.theglobeandmail.com",
            "category": "general",
            "language": "en",
            "country": "ca"
        }
    ]
    return {
        "status": "ok",
        "sources": response[:size]
    }


def newsapi_everything_response(article_number, total_result):
    articles = []
        
    for _ in range(article_number):
        article = {
            "source": {
                "id": None,
                "name": random_string(10) + ".com"
            },
            "author": random_string(15),
            "title": random_string(30),
            "description": random_string(50),
            "url": f"https://{random_string(10)}.com/{random_string(5)}",
            "urlToImage": f"https://{random_string(10)}.com/{random_string(5)}.jpg",
            "publishedAt": (
                datetime.utcnow() - timedelta(days=random.randint(20, 100))
            ).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "content": random_string(200)
        }
        articles.append(article)
    
    response = {
        "status": "ok",
        "totalResults": total_result,
        "articles": articles
    }
    return response 


class NewsSourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.NewsSource

    id = factory.Sequence(lambda n: f"news-source-{n}")
    name = factory.Faker('company')
    description = factory.Faker('text', max_nb_chars=200)
    url = factory.Faker('url')
    category = factory.Faker('word')
    language = factory.Faker('language_code')
    country = factory.Faker('country_code')


class NewsChannelFetchLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.NewsChannelFetchLog

    date_from = factory.LazyFunction(lambda: timezone.now() - datetime.timedelta(days=1))
    date_to = factory.LazyFunction(timezone.now)
    channel_name = NewsChannels.NEWSAPI.value
    source = factory.SubFactory(NewsSourceFactory)
    success = True
    exception = None


def chatgpt_respones():
    rs = f"Title: {random_string(20)}\n"
    rs += f"Description: {random_string(20)}\n"
    rs += f"Content: {random_string(100)}\n"
    return {'choices': [{'message': {'content': rs}}]}


def make_article(serial=1, title=None):
    return Article(
        author=f'test author {serial}',
        published_at=timezone.now() - timedelta(days=3),
        title=title or f'test title {serial}',
        content=f'test content {serial}',
        response={'t': f'test response {serial}'},
        description=f'test description {serial}',
    )


def make_article_page(article_num, page_number, source_id):
    return ArticlePage(
        page_number=page_number,
        channel='test',
        articles=[make_article(i) for i in range(1, article_num+1) ],
        source_id=source_id
    )


class ArticleRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ArticleRecord

    id = factory.Faker('uuid4')
    source = factory.SubFactory(NewsSourceFactory)
    author = factory.Faker('name')
    published_at = timezone.now()
    title = factory.Faker('sentence')
    content = factory.Faker('paragraph')
    description = factory.Faker('paragraph', nb_sentences=3, variable_nb_sentences=True)
    channel_name = factory.Faker('word')
    channel_response = factory.LazyFunction(lambda: {"key": "value"})  # Example JSON response
    url = factory.Faker('url')
    image_url = factory.Faker('url')
    title_bad_words = None 


class ModifiedArticleRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ModifiedArticleRecord

    id = factory.LazyFunction(uuid.uuid4)
    article = factory.SubFactory(ArticleRecordFactory)
    title = factory.Faker('sentence')
    content = factory.Faker('paragraph')
    description = factory.Faker('paragraph')
