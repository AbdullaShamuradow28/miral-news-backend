from rest_framework import serializers
from .models import Article, TemporaryArticle, Category
from datetime import timedelta
from django.utils import timezone

class ArticleSerializer(serializers.ModelSerializer):
    formatted_created_at = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'image', 'title', 'content', 'category', 'author', 'created_at', 'updated_at', 'formatted_created_at', 'authorMid'] # Add formatted_created_at

    def get_formatted_created_at(self, obj):
        now = timezone.now()
        created_at = obj.created_at

        diff = now - created_at

        if diff < timedelta(minutes=1):
            return "just now"
        elif diff < timedelta(hours=1):
            minutes = diff.seconds // 60
            return f"{minutes} minutes ago"
        elif diff < timedelta(days=1):
            hours = diff.seconds // 3600
            return f"{hours} hours ago"
        elif diff < timedelta(weeks=1):
            days = diff.days
            return f"{days} days ago"
        elif diff < timedelta(weeks=4):
            weeks = diff.days // 7
            return f"{weeks} weeks ago"
        else:
            return created_at.strftime("%d.%m.%Y %H:%M")

class TemporaryArticleSerializer(serializers.ModelSerializer):
    formatted_created_at = serializers.SerializerMethodField()

    class Meta:
        model = TemporaryArticle
        fields = ['id', 'image', 'title', 'content', 'category', 'author', 'created_at', 'updated_at', 'formatted_created_at'] # Add formatted_created_at

    def get_formatted_created_at(self, obj):
        now = timezone.now()
        created_at = obj.created_at

        diff = now - created_at

        if diff < timedelta(minutes=1):
            return "just now"
        elif diff < timedelta(hours=1):
            minutes = diff.seconds // 60
            return f"{minutes} minutes ago"
        elif diff < timedelta(days=1):
            hours = diff.seconds // 3600
            return f"{hours} hours ago"
        elif diff < timedelta(weeks=1):
            days = diff.days
            return f"{days} days ago"
        elif diff < timedelta(weeks=4):
            weeks = diff.days // 7
            return f"{weeks} weeks ago"
        else:
            return created_at.strftime("%d.%m.%Y %H:%M")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']
