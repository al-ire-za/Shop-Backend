from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone_number', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]

admin.site.register(Cart)