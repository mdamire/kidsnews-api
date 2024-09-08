from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters import rest_framework as filters
from django.shortcuts import render, get_object_or_404

from .models import ArticleRecord, NewsSource
from .serializers import ArticleRecordSerializer


class ArticleRecordFilter(filters.FilterSet):
    published_at_gte = filters.DateTimeFilter(field_name='published_at', lookup_expr='gte')
    published_at_lte = filters.DateTimeFilter(field_name='published_at', lookup_expr='lte')
    source = filters.ModelChoiceFilter(queryset=NewsSource.objects.all(), field_name='source')

    class Meta:
        model = ArticleRecord
        fields = ['author', 'published_at']


# REST Views

class ArticleRecordListView(ListAPIView):
    queryset = ArticleRecord.objects.filter(
        modified_record__isnull=False
    ).select_related('modified_record')
    serializer_class = ArticleRecordSerializer
    filterset_class = ArticleRecordFilter
    search_fields = ('modified_record__title',)


class ArticleRecordDetailView(RetrieveAPIView):
    queryset = ArticleRecord.objects.filter(
        modified_record__isnull=False
    ).select_related('modified_record')
    serializer_class = ArticleRecordSerializer
    lookup_field = 'id'


# HTTP Views

def article_list_view(request):
    filterset = ArticleRecordFilter(request.GET, queryset=ArticleRecord.objects.filter(
        modified_record__isnull=False).select_related('modified_record', 'source'))
    
    context = {
        'filterset': filterset,
        'articles': filterset.qs  # Filtered queryset
    }
    return render(request, 'article/article_list.html', context)


def article_detail_view(request, id):
    article = get_object_or_404(ArticleRecord, id=id, modified_record__isnull=False)
    
    context = {
        'article': article
    }
    return render(request, 'article/article_detail.html', context)
