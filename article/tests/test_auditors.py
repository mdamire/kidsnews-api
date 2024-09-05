import unittest
from unittest.mock import MagicMock
from article.article import ArticlePage, Article
from article.auditors import check_article_title_for_bad_words 

class TestCheckArticleTitleForBadWords(unittest.TestCase):
    def setUp(self):
        # Create mock articles with different titles
        self.article1 = MagicMock(spec=Article)
        self.article1.title = "The dangers of smoking and alcohol"
        self.article1.set_title_bad_words = MagicMock()

        self.article2 = MagicMock(spec=Article)
        self.article2.title = "Healthy Eating Tips for Kids"
        self.article2.set_title_bad_words = MagicMock()

        self.article3 = MagicMock(spec=Article)
        self.article3.title = "Crime rates are rising due to drug abuse"
        self.article3.set_title_bad_words = MagicMock()

        # Create an ArticlePage mock
        self.article_page = MagicMock(spec=ArticlePage)
        self.article_page.articles = [self.article1, self.article2, self.article3]

    def test_check_article_title_for_bad_words(self):
        # Run the function with the mocked ArticlePage
        result = check_article_title_for_bad_words(self.article_page)

        # Check if the result is the same as the input ArticlePage
        self.assertEqual(result, self.article_page)

        # Check that set_title_bad_words was called with the correct bad words for each article
        self.article1.set_title_bad_words.assert_called_once_with(['smoking', 'alcohol'])
        self.article2.set_title_bad_words.assert_not_called()  # No bad words, should not be called
        self.article3.set_title_bad_words.assert_called_once_with(['Crime', 'drug', 'abuse'])
