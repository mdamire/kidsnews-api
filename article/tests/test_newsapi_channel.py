import asyncio
from unittest.mock import patch
from datetime import timedelta

from django.test import TestCase, override_settings
from django.utils import timezone

from article.channel.newsapi import handlers
from article.channel.article import ArticlePage
from article.models import ArticleRecord
from . import factories


@override_settings(TNA_API_KEY='test')
class TestChannelHandlers(TestCase):

    def test_async_get_article_pages(self):
        with patch('article.channel.newsapi.client.aiohttp.ClientSession.get') as patched:
            patched.return_value = factories.NewsAPIResponseFactory(520)

            article_pages = asyncio.run(
                handlers.async_get_article_pages(
                    timezone.now() - timedelta(days=10),
                    timezone.now() - timedelta(days=8)
                )
            )
            
            self.assertEqual(len(article_pages), 6)
            for i in article_pages:
                self.assertIsInstance(i, ArticlePage)

        # create the database
        asyncio.run(article_pages[0].abulk_create())
        self.assertEqual(ArticleRecord.objects.all().count(), 100)
