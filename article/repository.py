from .models import ArticleRecord
from django.db import transaction
from asgiref.sync import sync_to_async


def article_record_bulk_update(records: list[ArticleRecord]):
    for record in records:
        ArticleRecord.objects.filter(reference=record.reference).update(
            modified_title=record.modified_title,
            modified_description=record.modified_description,
            modified_content=record.modified_content,
            title_bad_words=record.title_bad_words,
            has_bad_words=record.has_bad_words,
            has_rewritten=record.has_rewritten
        )


async def article_record_abulk_update(records: list[ArticleRecord]):
    """
    Asynchronously saves a list of ArticleRecord instances to the database in bulk.
    """
    await sync_to_async(article_record_bulk_update)(records)
