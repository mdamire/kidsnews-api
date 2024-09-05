from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.utils import timezone

from article.tasks import featch_and_rewrite_news_articles
from article.models import ArticleRecord
from . import factories

@override_settings(TNA_API_KEY='test', CHATGPT_API_KEY='test')
class TestTasks(TestCase):
    
    def test_featch_and_rewrite_news_articles(self):

        with (
            patch('article.channel.newsapi.client.aiohttp.ClientSession.get') as channel_patched,
            patch('article.rewrite.chatgpt.client.aiohttp.ClientSession.post') as rewrite_patched
        ):
            channel_patched.return_value = factories.NewsAPIResponseFactory(52, 52)
            rewrite_patched.return_value = factories.ChatGptResponseFactory(52)

            count = featch_and_rewrite_news_articles(
                timezone.now()-timedelta(days=10),
                timezone.now()-timedelta(days=8)
            )
            # self.assertEqual(ArticleRecord.objects.all().count(), 52)

            self.assertEqual(count, 52)