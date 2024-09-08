from rest_framework import serializers
from .models import ArticleRecord, ModifiedArticleRecord


class ArticleRecordSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

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

    def get_title(self, obj):
        if hasattr(obj, 'modified_record'):
            return obj.modified_record.title
        return obj.title

    def get_description(self, obj):
        if hasattr(obj, 'modified_record'):
            return obj.modified_record.description
        return obj.description

    def get_content(self, obj):
        if hasattr(obj, 'modified_record'):
            return obj.modified_record.content
        return obj.content
