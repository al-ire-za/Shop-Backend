from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from django.db.models.functions import Coalesce
from .models import Category, Product, ProductComment
from .serializers import CategorySerializer, ProductSerializer, CommentSerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name']
    ordering_fields = ['price', 'created_at', 'avg_rating']

    def get_queryset(self):
        return Product.objects.annotate(
            avg_rating=Coalesce(Avg('comments__rating'), 5.0)
        )

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class AddCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        if user:
            user_name = user.get_full_name().strip() or user.username
        else:
            user_name = 'کاربر مهمان'
        serializer.save(user=user, user_name=user_name)