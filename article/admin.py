from django.contrib import admin

from . import models


@admin.register(models.ArticleRecord)
class ArticleRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'published_at', 'title', '_has_rewritten')
    readonly_fields = ('_modified_title', '_modified_content', '_modified_description')
    search_fields = ('author', 'title', 'title')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('modified_record')

    def _has_rewritten(self, obj):
        return bool(hasattr(obj, 'modified_record') and obj.modified_record)
    _has_rewritten.boolean=True

    def _modified_title(self, obj):
        if not obj.modified_record:
            return None
        return obj.modified_record.title
    
    def _modified_content(self, obj):
        if not obj.modified_record:
            return None
        return obj.modified_record.content
    
    def _modified_description(self, obj):
        if not obj.modified_record:
            return None
        return obj.modified_record.description


@admin.register(models.NewsChannelFetchLog)
class NewsChannelFetchLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'channel_name', 'date_from', 'date_to', 'source', 'success')


@admin.register(models.NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

