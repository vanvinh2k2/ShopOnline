from rest_framework import serializers
from .models import *

class UserSeriallizes(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'is_active': {'read_only': True},
            'date_joined': {'read_only': True},
        }

class LoginUserSeriallizes(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'is_active': {'read_only': True},
            'date_joined': {'read_only': True},
            'username': {'read_only': True},
        }