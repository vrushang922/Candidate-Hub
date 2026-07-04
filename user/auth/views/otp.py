from rest_framework import status
from rest_framework.response import Response
from ..serializers.otp import OTPRegisterSerializer, OTPSendSerializer
from rest_framework.views import APIView
from ..services.otp_service import generate_otp, save_otp, verify_otp, send_otp_email
from django.utils import timezone
from ...models import User
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken



class RegisterOTPSentView(APIView):
    throttle_scope = 'otp_send'

    def post(self, request):
        serializer = OTPRegisterSerializer(data=request.data)
        if serializer.is_valid():
            otp = generate_otp()
            email = serializer.validated_data['email']
            send_otp_email(email,otp)
            save_otp(email, otp)
            return Response('OTP sent successfully', status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterOTPVerifyView(APIView):
    throttle_scope = 'otp_verify'

    def post(self, request):
        otp = str(request.data.pop('otp'))
        serializer = OTPRegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if verify_otp(email, otp):
                user = serializer.save()
                user.mark_email_verified()
                user.save()
                return Response('User registered successfully', status=status.HTTP_201_CREATED)

        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginOTPSendView(APIView):
    throttle_scope = 'otp_send'

    def post(self, request):
        serializer = OTPSendSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects.filter(email=email).exists():
                otp = generate_otp()
                send_otp_email(email, otp)
                save_otp(email, otp)
                return Response('OTP sent successfully', status = status.HTTP_200_OK)
            
            else:
                raise ValidationError("User not found")
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class LoginOTPVerifyView(APIView):
    throttle_scope = 'otp_verify'


    def post(self, request):
        otp = request.data.get("otp")

        serializer = OTPSendSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        email = serializer.validated_data["email"]
        user = get_object_or_404(User, email= email)

        if verify_otp(email, otp):
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            return Response({"status": "Login successful", "access": access, "refresh": str(refresh)}, status = status.HTTP_200_OK)
        else:
            raise ValidationError("email or otp invalid")


