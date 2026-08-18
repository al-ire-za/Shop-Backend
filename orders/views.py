from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, CartItem, Order
from .serializers import CartSerializer, OrderSerializer, CartItemSerializer
from products.models import Product

class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # ۱. دریافت سبد خرید کاربر
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemSerializer(cart.items.select_related('product').all(), many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ۲. افزودن کالا به سبد خرید
    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({'error': 'شناسه محصول الزامی است.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'محصول مورد نظر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response({'message': 'محصول به سبد خرید اضافه شد.'}, status=status.HTTP_200_OK)

    # ۳. تغییر تعداد یا حذف کالا
    def patch(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 0))

        cart, _ = Cart.objects.get_or_create(user=request.user)
        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
            return Response({'message': 'تغییرات با موفقیت اعمال شد.'}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': 'آیتم مورد نظر در سبد یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)


class CreateOrderView(generics.CreateAPIView):
    """
    ثبت سفارش هم برای کاربر لاگین‌شده و هم کاربر مهمان با ثبت مشخصات تحویل
    """
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        order = serializer.save(user=user)

        # اگر کاربر وارد حساب شده بود، سبد خرید دیتابیس او پس از ثبت سفارش تخلیه شود
        if user:
            try:
                cart = Cart.objects.get(user=user)
                cart.items.all().delete()
            except Cart.DoesNotExist:
                pass

