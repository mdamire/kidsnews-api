from django.test import TestCase
from unittest.mock import MagicMock
from article.models import ArticleRecord
from article.auditors import check_article_title_for_bad_words

class TestCheckArticleTitleForBadWords(TestCase):
    def setUp(self):
        # Create mock ArticleRecord objects with different original titles
        self.article1 = MagicMock(spec=ArticleRecord)
        self.article1.original_title = "The dangers of smoking and alcohol"
        self.article1.set_title_bad_words = MagicMock()

        self.article2 = MagicMock(spec=ArticleRecord)
        self.article2.original_title = "Healthy Eating Tips for Kids"
        self.article2.set_title_bad_words = MagicMock()

        self.article3 = MagicMock(spec=ArticleRecord)
        self.article3.original_title = "Crime rates are rising due to drug abuse"
        self.article3.set_title_bad_words = MagicMock()

        # List of ArticleRecord mock objects
        self.article_records = [self.article1, self.article2, self.article3]

    def test_check_article_title_for_bad_words(self):
        # Run the function with the list of mocked ArticleRecord objects
        result = check_article_title_for_bad_words(self.article_records)

        # Check if the result is the same as the input list of ArticleRecord objects
        self.assertEqual(result, self.article_records)

        # Check that set_title_bad_words was called with the correct bad words for each article
        self.article1.set_title_bad_words.assert_called_once_with(['smoking', 'alcohol'])
        self.article2.set_title_bad_words.assert_not_called()  # No bad words, should not be called
        self.article3.set_title_bad_words.assert_called_once_with(['Crime', 'drug', 'abuse'])
