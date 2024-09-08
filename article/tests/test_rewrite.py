from unittest.mock import patch
import logging

from django.test import TestCase, override_settings

from article.rewrite import handlers
from article import models
from . import factories

@override_settings(CHATGPT_API_KEY='test')
class TestChatGptHandlers(TestCase):
    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)

    def test_rewrite_articles(self):
        a1 = factories.ArticleRecordFactory()
        a2 = factories.ArticleRecordFactory(title='murder title')
        a3 = factories.ArticleRecordFactory()

        with patch('article.rewrite.chatgpt.handlers.send_request_to_chatgpt') as c_patched:
            c_patched.return_value = factories.chatgpt_respones()
            handlers.rewrite_articles([a1, a2, a3])

            self.assertEqual(models.ModifiedArticleRecord.objects.count(), 2)

        r_a1 = models.ArticleRecord.objects.get(id=a1.id)
        r_a2 = models.ArticleRecord.objects.get(id=a2.id)

        self.assertIsNone(r_a1.title_bad_words)
        self.assertIsNotNone(r_a2.title_bad_words)
