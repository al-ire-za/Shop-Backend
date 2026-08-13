from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, ProductComment
from .serializers import CategorySerializer, ProductSerializer, CommentSerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name']
    ordering_fields = ['price', 'created_at', 'rating']

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class AddCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        user_name = self.request.user.get_full_name() if user else 'کاربر مهمان'
        serializer.save(user=user, user_name=user_name)