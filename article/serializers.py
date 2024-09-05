from rest_framework import serializers
from .models import ArticleRecord


class ArticleRecordSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='modified_title', read_only=True)
    description = serializers.CharField(source='modified_description', read_only=True, allow_null=True)
    content = serializers.CharField(source='modified_content', read_only=True)

    class Meta:
        model = ArticleRecord
        fields = [
            'id',
            'author',
            'published_at',
            'title',
            'description',
            'content',
            'channel_name',
            'url',
            'image_url'
        ]
