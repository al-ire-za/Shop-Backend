from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Address

User = get_user_model()

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'title', 'full_address', 'postal_code', 'city', 'province']

class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'addresses']
        read_only_fields = ['id', 'role']