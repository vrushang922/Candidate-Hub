from rest_framework import serializers
from ...models import User

class OTPRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value
    
    def create(self, validated_data):
        email = validated_data['email']
        user = User(email=email)
        user.set_unusable_password()
        user.save()
        return user
    
    class Meta:
        model = User
        fields = ['email']

class OTPSendSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["email"]





class OTPLoginserializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email is not registered.")
        
        # Here you would add logic to verify the OTP for the given email
        # For example, you might check a cache or database for the OTP associated with the email

        return data