from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', ArticleListCreate.as_view(), name='article-list-create'),
    path('search/', ArticleSearchList.as_view(), name='article-search'), # New search path
    path('<int:pk>/', ArticleRetrieveUpdateDestroy.as_view(), name='article-retrieve-update-destroy'),
    path('<int:pk>/delete/', ArticleDestroy.as_view(), name='article-destroy'),
    path('temporary/', TemporaryArticleListCreate.as_view(), name='temporary-article-list-create'),
    path('categories/', CategoriesList.as_view(), name='categories-list'),
    path('temporary/<int:pk>/', TemporaryArticleRetrieveUpdateDestroy.as_view(), name='temporary-article-retrieve-update-destroy'),
]