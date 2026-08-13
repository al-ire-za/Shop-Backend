from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from orders.models import Cart, CartItem
from .models import Address

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    لگین کاربر و ادغام سبد خرید مهمان (Guest LocalStorage) با سبد خرید سمت سرور
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(email=request.data.get('email'))
            guest_cart_data = request.data.get('guest_cart', {}) # ساختار: {"product_id": quantity}

            if guest_cart_data:
                user_cart, _ = Cart.objects.get_or_create(user=user)
                for product_id, qty in guest_cart_data.items():
                    cart_item, created = CartItem.objects.get_or_create(
                        cart=user_cart,
                        product_id=product_id,
                        defaults={'quantity': qty}
                    )
                    if not created:
                        cart_item.quantity += qty
                        cart_item.save()

        return response

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user