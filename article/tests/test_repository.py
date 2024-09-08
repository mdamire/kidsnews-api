from django.test import TestCase
import logging

from article import repository, models
from . import factories


class TestRepository(TestCase):
    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)

    def test_save_article_pages(self):
        source = factories.NewsSourceFactory()

        ap1 = factories.make_article_page(3, 1, source.id)
        records = repository.save_article_pages([ap1])
        self.assertTrue(records[0].id)
        self.assertEqual(len(records), 3)
        self.assertEqual(models.ArticleRecord.objects.count(), 3)

        ap1.articles.append(factories.make_article(5))
        records = repository.save_article_pages([ap1])
        self.assertTrue(records[0].id)
        self.assertEqual(len(records), 4)
        self.assertEqual(models.ArticleRecord.objects.count(), 4)
