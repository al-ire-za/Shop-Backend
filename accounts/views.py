from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from orders.models import Cart, CartItem
from .models import Address
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    لاگین کاربر با username و ادغام سبد خرید محلی
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # جستجوی کاربر بر اساس username ارسالی
            username = request.data.get('username')
            user = User.objects.filter(username=username).first()

            guest_cart_data = request.data.get('guest_cart', {})  # ساختار: {"product_id": quantity}

            if user and guest_cart_data:
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
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)