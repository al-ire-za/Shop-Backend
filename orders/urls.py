from django.urls import path
from .views import CartView, CreateOrderView, UserOrdersListView, ApplyCouponView

urlpatterns = [
    path('cart/', CartView.as_view(), name='user-cart'),
    path('orders/create/', CreateOrderView.as_view(), name='create-order'),
    path('orders/my-orders/', UserOrdersListView.as_view(), name='my-orders'),
    path('orders/apply-coupon/', ApplyCouponView.as_view(), name='apply-coupon'),
]