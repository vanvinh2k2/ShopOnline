from rest_framework import serializers
from .models import *
from django.utils import timezone

class RegisterUserSeriallize(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(default=timezone.now)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active', 'date_joined', 'last_login']

class LoginUserSeriallize(serializers.ModelSerializer):
    password = serializers.CharField()
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['email', 'password']
