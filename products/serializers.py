from rest_framework import serializers
from .models import Category, Product, ProductAttribute, ProductComment, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['key', 'value']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProductComment
        fields = ['id', 'product', 'user', 'user_name', 'rating', 'text', 'created_at']
        read_only_fields = ['id', 'user', 'user_name', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    final_price = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 
            'name', 
            'category', 
            'price', 
            'discount_percent', 
            'final_price', 
            'is_new', 
            'is_bestseller', 
            'image', 
            'images',
            'rating', 
            'colors', 
            'attributes', 
            'comments'
        ]