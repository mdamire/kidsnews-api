"""
URL configuration for kidsnews project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from article.views import (
    ArticleRecordListView, ArticleRecordDetailView, article_list_view, article_detail_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/articles', ArticleRecordListView.as_view(), name='article-list'),
    path('api/articles/<uuid:id>', ArticleRecordDetailView.as_view(), name='article-detail'),

    path('articles/', article_list_view, name='article-list-http'),
    path('articles/<str:id>/', article_detail_view, name='article-detail-http'),
]
