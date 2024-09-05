import logging
import asyncio

from .channel.newsapi.handlers import async_get_article_pages
from .channel.article import ArticlePage
from .auditors import check_article_title_for_bad_words
from .repository import abulk_save
from .rewrite.chatgpt.handlers import rewrite_articles_for_kids


_log = logging.getLogger(__name__)


async def save_rewrite_save(article_page: ArticlePage):
    # save featched data
    article_objs = await article_page.abulk_create()

    # write in fetch log
    ...

    # audit for words
    article_objs = check_article_title_for_bad_words(article_objs)

    # rewrite contents
    article_objs = await rewrite_articles_for_kids()
    
    # save contents
    await abulk_save(article_objs)

    # update featched data


def featch_and_rewrite_news_articles(date_from, date_to):
    # fetch data from channel
    article_pages = asyncio.run(async_get_article_pages(date_from, date_to))

    coro_tasks = [
        save_rewrite_save(article_page)
        for article_page in article_pages
    ]
    asyncio.run(asyncio.gather(*coro_tasks))
    