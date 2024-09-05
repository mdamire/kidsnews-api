import re


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

        if _is_url(url):
            self.url = url
        else:
            self.url = None
        
        if _is_url(image_url):
            self.image_url = image_url
        else:
            self.image_url = None


class ArticlePage():
    def __init__(self, page_number: int, channel: str, articles: list[Article]):
        self.page_number = page_number
        self.channel_name = channel
        self.articles = articles
