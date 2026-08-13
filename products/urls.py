from django.urls import path
from .views import CategoryListView, ProductListView, ProductDetailView, AddCommentView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('comments/add/', AddCommentView.as_view(), name='add-comment'),
]