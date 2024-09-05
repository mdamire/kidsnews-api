import uuid
import random
from datetime import datetime, timedelta
from django.utils import timezone
import factory
from factory.django import DjangoModelFactory

from article.models import ArticleRecord
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


class NewsAPIResponseFactory(AsyncResponseFactory):
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
        model = ArticleRecord

    reference = factory.LazyFunction(uuid.uuid4)
    
    author = factory.Faker('name')
    published_at = factory.LazyFunction(timezone.now)

    original_title = factory.Faker('sentence')
    original_content = factory.Faker('paragraph')

    channel_name = factory.Faker('word')
    channel_response = factory.Faker('json')

    has_bad_words = False

    has_rewritten = False
