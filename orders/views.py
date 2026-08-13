from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Cart, CartItem, Order
from .serializers import CartSerializer, OrderSerializer

class CartView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

class CreateOrderView(generics.CreateAPIView):
    """
    ثبت سفارش هم برای کاربر لاگین‌شده و هم کاربر مهمان با ثبت مشخصات تحویل
    """
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)