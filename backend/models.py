from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    authorMid = models.CharField(max_length=6, null=True, blank=True)
    title = models.CharField(max_length=555)
    content = models.TextField()
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=180, null=True, blank=True) # Corrected category field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.CharField(max_length=20) # temporary
    comment = models.TextField()
    date_of_publishing = models.DateTimeField(auto_now_add=True)
    likes_counter = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])


# Временно, но надо обязательно

class TemporaryArticle(models.Model):
    title = models.CharField(max_length=555)
    content = models.TextField()
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, default="Статьи", null=True, blank=True, related_name='articles_t') # Corrected category field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
