import re
import uuid


def _is_url(url):
    url_regex = re.compile(
        r'^(https?://)?(\w+\.)?[\w-]+\.[a-z]+(/\S*)?$'
    )
    return re.match(url_regex, url) is not None


class Article():
    def __init__(
        self, author, published_at, title, content, response, description=None, 
        url=None, image_url=None, title_bad_words=[]
    ):
        self.author = author
        self.published_at = published_at
        self.title = title
        self.content = content
        self.response = response
        self.description = description

        self.title_bad_words = title_bad_words
        self.has_bad_words = False

        self.modified_title = None
        self.modified_content = None
        self.modified_description = None

        if url and _is_url(url):
            self.url = url
        else:
            self.url = None
        
        if image_url and _is_url(image_url):
            self.image_url = image_url
        else:
            self.image_url = None
    
    def set_title_bad_words(self, bad_words: list):
        self.title_bad_words = bad_words
        self.has_bad_words = True


class ArticlePage():
    def __init__(self, page_number: int, channel: str, articles: list[Article]):
        self.page_number = page_number
        self.channel_name = channel
        self.articles = articles
