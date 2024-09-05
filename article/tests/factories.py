import random
from unittest.mock import AsyncMock
from datetime import datetime, timedelta


def random_string(length=10):
    return ''.join(
        random.choices(
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 
            k=length
        )
    )


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
    
    async def __aenter__(self):
        # This method will be used in the async context manager
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        # important to mock asyncio context
        pass


