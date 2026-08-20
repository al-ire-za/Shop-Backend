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


class UserOrdersListView(generics.ListAPIView):
    """
    دریافت لیست سفارش‌های کاربر لاگین شده
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product').order_by('-created_at')


class ApplyCouponView(APIView):
    """
    بررسی و اعمال کد تخفیف
    """
    VALID_COUPONS = {
        'OFF10': {'percent': 10, 'min_amount': 0, 'max_discount': 500000},
        'OFF20': {'percent': 20, 'min_amount': 0, 'max_discount': 1000000},
        'WELCOME': {'percent': 15, 'min_amount': 0, 'max_discount': 750000},
        'SPRING': {'percent': 25, 'min_amount': 1000000, 'max_discount': 2000000},
    }

    def post(self, request):
        code = str(request.data.get('code', '')).strip().upper()
        if not code:
            return Response({'message': 'لطفاً کد تخفیف را وارد کنید.'}, status=status.HTTP_400_BAD_REQUEST)

        if code not in self.VALID_COUPONS:
            return Response({'message': 'کد تخفیف وارد شده نامعتبر یا منقضی شده است.'}, status=status.HTTP_404_NOT_FOUND)

        coupon_info = self.VALID_COUPONS[code]
        # در صورتی که مبلغ سفارش هم ارسال شده بود، مبلغ تخفیف محاسبه می‌شود
        total_price = int(request.data.get('total_price', 0))
        if total_price > 0:
            calc_discount = int(total_price * (coupon_info['percent'] / 100))
            discount_amount = min(calc_discount, coupon_info['max_discount'])
        else:
            # تخفیف پیش‌فرض تخمینی یا درصدی
            discount_amount = coupon_info['percent'] * 10000

        return Response({
            'valid': True,
            'code': code,
            'percent': coupon_info['percent'],
            'discount_amount': discount_amount,
            'message': f'کد تخفیف {coupon_info["percent"]} درصدی با موفقیت اعمال گردید.'
        }, status=status.HTTP_200_OK)

