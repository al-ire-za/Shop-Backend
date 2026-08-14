from django.db import models
from django.db.models import Avg
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
    colors = models.JSONField('Available Colors', default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        return int(self.price * (1 - self.discount_percent / 100))

    # محاسبه میانگین امتیاز نظرات به صورت خودکار
    @property
    def rating(self):
        # میانگین امتیاز تمام کامنت‌های تایید شده/ثبت شده برای این محصول
        avg_rating = self.comments.aggregate(Avg('rating'))['rating__avg']
        if avg_rating is not None:
            return round(avg_rating, 1)
        return 5.0  # امتیاز پیش‌فرض در صورت نبود نظر

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    key = models.CharField('Attribute Key', max_length=100)
    value = models.CharField('Attribute Value', max_length=255)

class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='Product')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='User')
    user_name = models.CharField('User Name', max_length=100, default='Guest User')
    rating = models.PositiveSmallIntegerField('Rating', default=5)
    text = models.TextField('Comment Text')
    created_at = models.DateTimeField('Created At', auto_now_add=True)

    class Meta:
        verbose_name = 'Product Comment'
        verbose_name_plural = 'Product Comments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user_name} on {self.product.name} (Rating: {self.rating})"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Product Image', upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"