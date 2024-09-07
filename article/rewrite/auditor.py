import re

from article.models import ArticleRecord


bad_words = [
    "violence", "murder", "kill", "death", "dead", "terror", "attack", "bomb", 
    "explosion", "drug", "narcotics", "abuse", "assault", "crime", "criminal", 
    "rape", "sexual", "harassment", "sex", "nude", "naked", "suicide", "self-harm", 
    "gun", "shoot", "weapon", "bloody", "blood", "racism", "racial", "discrimination", 
    "alcohol", "beer", "liquor", "tobacco", "smoke", "smoking", "gambling", 
    "addiction", "hate", "slavery", "bully", "bullying", "porn", "pornography", 
    "explicit", "profanity", "curse", "swear", "fight", "fighting", "hate speech"
]
bad_words_re_pattern = re.compile("|".join(bad_words), re.IGNORECASE)


def check_article_title_for_bad_words(article_records: list[ArticleRecord]) -> list[ArticleRecord]:
    for article in article_records:
        title_bad_words = re.findall(bad_words_re_pattern, article.title)
        if title_bad_words:
            article.title_bad_words = title_bad_words
            article.save()
    
    return article_records
