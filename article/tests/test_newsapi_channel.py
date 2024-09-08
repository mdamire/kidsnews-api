from unittest.mock import patch, call
from datetime import timedelta
import logging

from django.test import TestCase, override_settings
from django.utils import timezone


from article.channel import handlers
from article.channel.article import ArticlePage
from article import models
from . import factories


@override_settings(TNA_API_KEY='test')
class TestChannelHandlers(TestCase):
    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)

    def test_fetch_article_pages_1_source(self):
        with (
            patch('article.channel.newsapi.handlers.NewsApiClient.get_sources') as s_patched,
            patch('article.channel.newsapi.handlers.NewsApiClient.get_everything') as e_patched
        ):
            s_patched.return_value = factories.newsapi_source_response()
            e_patched.return_value = factories.newsapi_everything_response(50, 50)

            article_pages_list = list(handlers.fetch_article_pages(
                timezone.now() - timedelta(days=10),
                timezone.now() - timedelta(days=8),
                ['ca'],
                ['en']
            ))
            
            self.assertEqual(len(article_pages_list), 1)
            self.assertEqual(len(article_pages_list[0]), 1)
            for i in article_pages_list[0]:
                self.assertIsInstance(i, ArticlePage)
            
            self.assertEqual(models.NewsApiFetchLog.objects.all().count(), 1)
            self.assertTrue(models.NewsApiFetchLog.success)

    def test_fetch_article_pages_3_source(self):
        with (
            patch('article.channel.newsapi.handlers.NewsApiClient.get_sources') as s_patched,
            patch('article.channel.newsapi.handlers.NewsApiClient.get_everything') as e_patched
        ):
            s_patched.return_value = factories.newsapi_source_response(3)
            e_patched.return_value = factories.newsapi_everything_response(100, 200)

            article_pages_list = list(handlers.fetch_article_pages(
                timezone.now() - timedelta(days=10),
                timezone.now() - timedelta(days=8),
                ['ca'],
                ['en']
            ))
            
            self.assertEqual(len(article_pages_list), 3)
            self.assertEqual(len(article_pages_list[0]), 2)
            for i in article_pages_list[0]:
                self.assertIsInstance(i, ArticlePage)
            
            self.assertEqual(models.NewsApiFetchLog.objects.all().count(), 3)
    
    def test_already_fetched_dates(self):
        dt1 = timezone.now() - timedelta(days=10)
        dt2 = timezone.now() - timedelta(days=9)
        source = factories.NewsSourceFactory(id='cbc-news')
        factories.NewsApiFetchLogFactory(
            source=source,
            date_from=dt2
        )
        with (
                patch('article.channel.newsapi.handlers.NewsApiClient.get_sources') as s_patched,
                patch('article.channel.newsapi.handlers.fetch_source_article_page') as f_patched

            ):
            s_patched.return_value = factories.newsapi_source_response(1)

            article_pages_list = list(handlers.fetch_article_pages(
                dt1,
                timezone.now() - timedelta(days=8),
                ['ca'],
                ['en']
            ))

            f_patched.assert_called_once_with(dt1, dt2, source.id, ['en'])
    
    def test_already_fetched_dates_multiple_sections(self):
        dt1 = timezone.now() - timedelta(days=10)
        dt2 = timezone.now() - timedelta(days=9)
        dt3 = timezone.now() - timedelta(days=8)
        dt4 = timezone.now() - timedelta(days=7)
        source = factories.NewsSourceFactory(id='cbc-news')
        factories.NewsApiFetchLogFactory(
            source=source,
            date_from=dt2,
            date_to=dt3
        )
        factories.NewsApiFetchLogFactory(
            source=source,
            date_from=dt4
        )
        with (
                patch('article.channel.newsapi.handlers.NewsApiClient.get_sources') as s_patched,
                patch('article.channel.newsapi.handlers.fetch_source_article_page') as f_patched

            ):
            s_patched.return_value = factories.newsapi_source_response(1)

            article_pages_list = list(handlers.fetch_article_pages(
                dt1,
                dt4,
                ['ca'],
                ['en']
            ))

            self.assertEqual(
                f_patched.call_args_list,
                [
                    call(dt1, dt2, source.id, ['en']),
                    call(dt3, dt4, source.id, ['en'])
                ]
            )

