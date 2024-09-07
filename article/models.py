import uuid

from django.db import models

from model_utils.models import TimeStampedModel


class NewsSource(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(max_length=500)
    category = models.CharField(max_length=100)
    language = models.CharField(max_length=10)
    country = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class NewsApiFetchLog(TimeStampedModel):
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()

    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE)

    success = models.BooleanField(default=False)
    exception = models.TextField(blank=True, null=True)


class ArticleRecord(TimeStampedModel):
    id = models.CharField(max_length=64, primary_key=True)
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE)

    author = models.CharField(max_length=500)
    published_at = models.DateTimeField()

    title = models.TextField()
    content = models.TextField()
    description = models.TextField(blank=True, null=True)

    channel_name = models.CharField(max_length=64)
    channel_response = models.JSONField()

    url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    title_bad_words = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title


class ModifiedArticleRecord(TimeStampedModel):
    original = models.OneToOneField(ArticleRecord, on_delete=models.CASCADE, related_name='modified_record')

    title = models.TextField()
    content = models.TextField()
    description = models.TextField(blank=True, null=True)

