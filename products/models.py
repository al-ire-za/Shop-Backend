from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField('Category Name', max_length=100)
    slug = models.SlugField(unique=True, allow_unicode=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Category')
    name = models.CharField('Product Name', max_length=255)
    price = models.PositiveIntegerField('Price (Toman)')
    discount_percent = models.PositiveIntegerField('Discount Percent', default=0)
    is_new = models.BooleanField('New Product', default=False)
    is_bestseller = models.BooleanField('Bestseller', default=False)
    image = models.ImageField('Product Image', upload_to='products/')
    rating = models.FloatField('Rating', default=5.0)
    
    # اضافه شدن فیلد رنگ‌ها
    # نمونه مقدار ذخیره‌شده: [{"name": "Black", "hex": "#000000"}, {"name": "Blue", "hex": "#2563eb"}]
    colors = models.JSONField('Available Colors', default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        return int(self.price * (1 - self.discount_percent / 100))

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    key = models.CharField('Attribute Key', max_length=100)
    value = models.CharField('Attribute Value', max_length=255)

class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    user_name = models.CharField('User Name', max_length=100, default='Guest User')
    rating = models.PositiveSmallIntegerField('Rating', default=5)
    text = models.TextField('Comment Text')
    created_at = models.DateTimeField(auto_now_add=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Product Image', upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"