from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product.id', read_only=True)
    name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.IntegerField(source='product.price', read_only=True)
    discount_percent = serializers.IntegerField(source='product.discount_percent', read_only=True)
    final_price = serializers.IntegerField(source='product.final_price', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'name', 'price', 'discount_percent', 'final_price', 'image', 'quantity']

    def get_image(self, obj):
        if obj.product.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.product.image.url) if request else obj.product.image.url
        return ''

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'full_name', 'phone_number', 'address', 'total_price', 'status', 'items', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return order