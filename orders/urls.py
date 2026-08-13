from django.urls import path
from .views import CartView, CreateOrderView

urlpatterns = [
    path('cart/', CartView.as_view(), name='user-cart'),
    path('orders/create/', CreateOrderView.as_view(), name='create-order'),
]