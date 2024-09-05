import asyncio
from unittest.mock import patch

from django.test import TestCase, override_settings

from article.rewrite.chatgpt import handlers
from . import factories

@override_settings(CHATGPT_API_KEY='test')
class TestChatGptHandlers(TestCase):

    def test_rewrite_articles_for_kids(self):

        article_records = [ factories.ArticleRecordFactory() for i in range(5)]

        with patch('article.rewrite.chatgpt.client.aiohttp.ClientSession.post') as patched:
            patched.return_value = factories.ChatGptResponseFactory(5)

            m_article_page = asyncio.run(
                handlers.rewrite_articles_for_kids(article_records)
            )

            for a in m_article_page:
                self.assertIsNotNone(a.modified_title)
                self.assertIsNotNone(a.modified_content)
                self.assertIsNotNone(a.modified_description)
