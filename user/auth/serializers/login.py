from rest_framework import serializers
from ...models import User
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


    class Meta:
        model = User
        fields = ['email', 'password']

        
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not User.objects.filter(email=email).exists():
            raise ValidationError({"email" :"Email is not registered."})
        
        user = User.objects.get(email=email)

        if not user.check_password(password):
            raise ValidationError({"password" :"Incorrect password."})
        
        return data




class PasswordSetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise ValidationError("Email is not registered.")
        return value
    
    def validate_password(self, value):
        validate_password(value)
        return value
    
    class Meta:
        model = User
        fields = ['email', 'password']
    