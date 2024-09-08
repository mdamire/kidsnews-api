from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.utils import timezone

from article import tasks
from article.models import ArticleRecord
from . import factories


@override_settings(TNA_API_KEY='test', CHATGPT_API_KEY='test')
class TestTasks(TestCase):
    
    def test_featch_and_rewrite_news_articles(self):
        
        with (
            patch('article.channel.newsapi.handlers.NewsApiClient.get_sources') as s_patched,
            patch('article.channel.newsapi.handlers.NewsApiClient.get_everything') as e_patched,
            patch('article.rewrite.chatgpt.handlers.send_request_to_chatgpt') as c_patched
        ):
            s_patched.return_value = factories.newsapi_source_response(2)
            e_patched.return_value = factories.newsapi_everything_response(48, 50)
            c_patched.return_value = factories.chatgpt_respones()

            count = tasks.fetch_and_rewrite_news_articles(
                timezone.now()-timedelta(days=10),
                timezone.now()-timedelta(days=8),
                ['ca'],
                ['en']
            )

            self.assertEqual(ArticleRecord.objects.all().count(), 96)
            self.assertEqual(count, 96)
