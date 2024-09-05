from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User

from . import factories


class TestEndpoints(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='tu', password='tp')
        self.r1 = factories.ArticleRecordFactory(
            published_at=timezone.now() - timedelta(days=10),
            modified_title='A common title',
            has_rewritten=True
        )
        self.r2 = factories.ArticleRecordFactory(
            published_at=timezone.now() - timedelta(days=8),
            has_rewritten=True,
            modified_title='test',
            modified_description='md'
        )
        self.r3 = factories.ArticleRecordFactory(
            published_at=timezone.now() - timedelta(days=6),
            has_rewritten=True
        )
        self.r4 = factories.ArticleRecordFactory(
            published_at=timezone.now() - timedelta(days=6),
        )
        self.client.login(username='tu', password='tp')

    def test_article_detail(self):
        url = reverse('article-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_article_filter(self):
        url = reverse('article-list') + f'?published_at_gte={self.r2.published_at.strftime("%Y-%m-%d")}'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_article_search(self):
        url = reverse('article-list') + f'?search=common'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_detail_record(self):
        """
        Ensure we can retrieve the detail of a specific record.
        """
        url = reverse('article-detail', args=[self.r2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], str(self.r2.id))
        self.assertEqual(response.data['title'], self.r2.modified_title)
