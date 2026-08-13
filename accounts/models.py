from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Username must be provided')
        if not email:
            raise ValueError('Email address must be provided')
            
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        CUSTOMER = 'CUSTOMER', 'Customer'

    email = models.EmailField('Email Address', unique=True)
    phone_number = models.CharField('Phone Number', max_length=11, blank=True, null=True)
    role = models.CharField('Role', max_length=10, choices=Role.choices, default=Role.CUSTOMER)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='User')
    title = models.CharField('Address Title', max_length=50)
    full_address = models.TextField('Full Address')
    postal_code = models.CharField('Postal Code', max_length=10)
    city = models.CharField('City', max_length=50)
    province = models.CharField('Province', max_length=50)

    def __str__(self):
        return f"{self.title} - {self.user.username}"