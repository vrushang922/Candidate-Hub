from rest_framework import serializers
from ...models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email = value).exists():
            raise ValidationError("Email is already registered.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value



    def create(self, validated_data, **kwargs):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'], **kwargs
        )
        return user
    
