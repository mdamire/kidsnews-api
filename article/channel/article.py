import re
import uuid

from article.models import ArticleRecord


def _is_url(url):
    url_regex = re.compile(
        r'^(https?://)?(\w+\.)?[\w-]+\.[a-z]+(/\S*)?$'
    )
    return re.match(url_regex, url) is not None


class Article():
    def __init__(
        self, author, published_at, title, content, response, description=None, 
        url=None, image_url=None
    ):
        self.author = author
        self.published_at = published_at
        self.title = title
        self.content = content
        self.response = response
        self.description = description
        self.reference = uuid.uuid4()

        if url and _is_url(url):
            self.url = url
        else:
            self.url = None
        
        if image_url and _is_url(image_url):
            self.image_url = image_url
        else:
            self.image_url = None


class ArticlePage():
    def __init__(self, page_number: int, channel: str, articles: list[Article]):
        self.page_number = page_number
        self.channel_name = channel
        self.articles = articles
    
    async def abulk_create(self):
        record_objs = [
            ArticleRecord(
                reference=article.reference,
                author=article.author,
                published_at=article.published_at,
                original_title=article.title,
                original_description=article.description,
                original_content=article.content,
                url=article.url,
                image_url=article.image_url,
                channel_name=self.channel_name,
                channel_response=article.response
            )
            for article in self.articles
        ]

        records = await ArticleRecord.objects.abulk_create(record_objs, ignore_conflicts=True)
        
        return records
