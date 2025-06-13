from rest_framework import generics
from .models import Article, TemporaryArticle, Category
from .serializers import ArticleSerializer, CategorySerializer, TemporaryArticleSerializer
from django.db.models import Q # Import Q object for complex lookups

class ArticleListCreate(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.all()

        # Handle 'category' filtering as before
        categories_param = self.request.query_params.get('category')
        if categories_param:
            category_names = [name.strip() for name in categories_param.split(',')]
            queryset = queryset.filter(category__in=category_names)

        return queryset

class ArticleSearchList(generics.ListAPIView): # New or modified view for search
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.all()
        # Get the 'query' parameter for full-text search
        search_query = self.request.query_params.get('query', None)

        if search_query:
            # Filter articles where title or content contains the search query (case-insensitive)
            # You can add more fields if needed (e.g., author, tags)
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            ).distinct() # Use .distinct() to avoid duplicate results if an article matches multiple Q conditions

        return queryset

class ArticleDestroy(generics.DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class TemporaryArticleListCreate(generics.ListCreateAPIView):
    queryset = TemporaryArticle.objects.all()
    serializer_class = TemporaryArticleSerializer

class TemporaryArticleRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = TemporaryArticle.objects.all()
    serializer_class = TemporaryArticleSerializer

class CategoriesList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer