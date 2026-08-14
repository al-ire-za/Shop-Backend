from django.contrib import admin
from .models import Category, Product, ProductAttribute, ProductComment, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # تعداد فرم‌های آماده برای آپلود عکس

class AttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1

# نمایش نظرات محصول به صورت جدول داخلی داخل صفحه خود محصول
class ProductCommentInline(admin.TabularInline):
    model = ProductComment
    extra = 0
    readonly_fields = ('user_name', 'rating', 'text', 'created_at')
    can_delete = True

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_percent', 'is_new', 'is_bestseller']
    list_filter = ['category', 'is_new', 'is_bestseller']
    search_fields = ['name']
    # اضافه شدن نظرات در کنار عکس‌ها و ویژگی‌ها به پنل ادمین محصول
    inlines = [ProductImageInline, AttributeInline, ProductCommentInline]

# شخصی‌سازی بخش نظرات برای نمایش خوانا و فیلتر بر اساس هر محصول
@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user_name', 'rating', 'short_text', 'created_at')
    list_filter = ('product', 'rating', 'created_at')  # سایدبار فیلتر بر اساس نام محصول
    search_fields = ('product__name', 'user_name', 'text')
    ordering = ('-created_at',)

    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    short_text.short_description = 'متن نظر'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}