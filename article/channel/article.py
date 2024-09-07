import re
import hashlib


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

        self.url = url if url and _is_url(url) else None
        self.image_url = image_url if image_url and _is_url(image_url) else None


class ArticlePage():
    def __init__(self, page_number: int, channel: str, articles: list[Article], source_id: str):
        self.page_number = page_number
        self.channel_name = channel
        self.articles = articles
        self.source_id = source_id
