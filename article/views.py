from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters import rest_framework as filters
from .models import ArticleRecord
from .serializers import ArticleRecordSerializer


class ArticleRecordFilter(filters.FilterSet):
    published_at = filters.DateFilter(field_name='published_at', lookup_expr='exact')
    published_at_gte = filters.DateTimeFilter(field_name='published_at', lookup_expr='gte')
    published_at_lte = filters.DateTimeFilter(field_name='published_at', lookup_expr='lte')

    class Meta:
        model = ArticleRecord
        fields = ['author', 'published_at']


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
