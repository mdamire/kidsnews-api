from django.db import models

from model_utils.models import TimeStampedModel


class ArticleRecord(models.Model):
    author = models.CharField(max_length=500)
    published_at = models.DateTimeField()

    original_title = models.TextField()
    modified_title = models.TextField(blank=True, null=True)

    original_description = models.TextField(blank=True, null=True)
    modified_description = models.TextField(blank=True, null=True)

    original_content = models.TextField()
    modified_content = models.TextField(blank=True, null=True)

    channel_name = models.CharField(max_length=64)
    channel_response = models.JSONField()

    url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    title_bad_words = models.CharField(max_length=200, blank=True, null=True)
    has_bad_words = models.BooleanField(default=False)

    has_rewritten = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_at']
    
    def set_title_bad_words(self, bad_words: list[str]):
        self.title_bad_words = ','.join(bad_words)
        self.has_bad_words = True

    def __str__(self):
        return self.modified_title or self.original_title



