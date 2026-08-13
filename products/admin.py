from django.contrib import admin
from .models import Category, Product, ProductAttribute, ProductComment, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # تعداد فرم‌های آماده برای آپلود عکس

class AttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_percent', 'is_new', 'is_bestseller']
    list_filter = ['category', 'is_new', 'is_bestseller']
    search_fields = ['name']
    inlines = [ProductImageInline, AttributeInline]  # افزودن عکس‌های متعدد به پنل ادمین

admin.site.register(Category)
admin.site.register(ProductComment)