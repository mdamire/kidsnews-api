from article.models import ArticleRecord

from .auditor import check_article_title_for_bad_words
from .chatgpt.handlers import rewrite_article_for_kids
from .enums import AIBots


def rewrite_articles(article_records: list[ArticleRecord], ai_bot=AIBots.chatgpt):
    if ai_bot not in AIBots:
        raise ValueError(f"Unkonwn ai bot: {ai_bot}")
    
    checked_records = check_article_title_for_bad_words(article_records)


    modified_records = []
    for article in checked_records:
        modified_records.append(rewrite_article_for_kids(article))
    
    return modified_records
