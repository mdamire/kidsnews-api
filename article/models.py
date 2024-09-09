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


class NewsChannelFetchLog(TimeStampedModel):
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    channel_name = models.CharField(max_length=200)

    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE)

    success = models.BooleanField(default=False)
    exception = models.TextField(blank=True, null=True)

    def fetched_articles(self):
        return ArticleRecord.objects.filter(fetch_log=self)

    # Function to return the number of modified articles
    def modified_articles(self):
        return ModifiedArticleRecord.objects.filter(article__fetch_log=self)

    # Function to return the number of articles that have title_bad_words
    def articles_with_bad_words(self):
        return ArticleRecord.objects.filter(
            fetch_log=self, title_bad_words__isnull=False
        ).exclude(
            title_bad_words__exact=''
        )


class ArticleRecord(TimeStampedModel):
    id = models.CharField(max_length=64, primary_key=True)
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE)
    fetch_log = models.ForeignKey(NewsChannelFetchLog, on_delete=models.SET_NULL, null=True, blank=True)

    author = models.CharField(max_length=500, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)

    title = models.TextField()
    content = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    channel_name = models.CharField(max_length=64)
    channel_response = models.JSONField()

    url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    title_bad_words = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        ordering = ['-published_at']
        constraints = [
            models.UniqueConstraint(fields=['source', 'title'], name='unique_source_title')
        ]
    
    def __str__(self):
        return self.title


class ModifiedArticleRecord(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    article = models.OneToOneField(
        ArticleRecord, on_delete=models.CASCADE, related_name='modified_record'
    )

    title = models.TextField()
    content = models.TextField()
    description = models.TextField(blank=True, null=True)
