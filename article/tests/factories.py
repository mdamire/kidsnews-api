import uuid
import random
from datetime import datetime, timedelta
from django.utils import timezone
import factory
from factory.django import DjangoModelFactory

from article import models
from article.channel.article import Article, ArticlePage


def random_string(length=10):
    return ''.join(
        random.choices(
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 
            k=length
        )
    )


class AsyncResponseFactory():
    async def __aenter__(self):
        # This method will be used in the async context manager
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        # important to mock asyncio context
        pass


class NewsAPIResponseFactory():
    def __init__(self, total_result, article_number=100, status=200):
        self.total_result = total_result
        self.article_number = article_number
        self.status = status

    def _generate_dummy_newsapi_response(self):
        articles = []
        
        for _ in range(self.article_number):
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
            "totalResults": self.total_result,
            "articles": articles
        }
        return response
    
    async def json(self):
        return self._generate_dummy_newsapi_response()


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


class NewsApiFetchLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.NewsApiFetchLog

    date_from = factory.LazyFunction(lambda: timezone.now() - datetime.timedelta(days=1))
    date_to = factory.LazyFunction(timezone.now)
    source = factory.SubFactory(NewsSourceFactory)
    success = True
    exception = None


class ChatGptResponseFactory(AsyncResponseFactory):
    def __init__(self, article_num, status=200) -> None:
        self.article_num = article_num
        self.status = 200
    
    def _single_dummy_response(self, id):
        rs = f"ID: {id}\n"
        rs += f"Title: {random_string(20)}\n"
        rs += f"Description: {random_string(20)}\n"
        rs += f"Content: {random_string(100)}\n\n"
        return rs
    
    def _generate_dummy_response(self):
        ct = ''
        for i in range(self.article_num):
            ct += self._single_dummy_response(i)
        
        response = {
            'choices': [
                {
                    'message': {
                        'content': ct
                    }
                }
            ]
        }

        return response
    
    async def json(self):
        return self._generate_dummy_response()


def make_article(serial=1):
    return Article(
        author=f'test author {serial}',
        published_at=timezone.now() - timedelta(days=3),
        title=f'test title {serial}',
        content=f'test content {serial}',
        response={f'test response {serial}'},
        description=f'test description {serial}',
    )

def make_article_page(article_num, page_number):
    return ArticlePage(
        page_number=page_number,
        channel='test',
        articles=[make_article(i) for i in range(1, article_num+1) ]
    )


class ArticleRecordFactory(DjangoModelFactory):
    class Meta:
        model = models.ArticleRecord

    reference = factory.LazyFunction(uuid.uuid4)
    
    author = factory.Faker('name')
    published_at = factory.LazyFunction(timezone.now)

    original_title = factory.Faker('sentence')
    original_content = factory.Faker('paragraph')

    channel_name = factory.Faker('word')
    channel_response = factory.Faker('json')

    has_bad_words = False

    has_rewritten = False
