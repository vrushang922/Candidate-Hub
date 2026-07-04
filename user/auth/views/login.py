from rest_framework.views import APIView
from rest_framework.response  import Response
from rest_framework import status
from ..serializers.login import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from ...models import User
from rest_framework.exceptions import ValidationError
from ..serializers.login import PasswordSetSerializer
# from rest_framework.renderers import JSONRenderer


class LoginView(APIView):
    # renderer_classes = [JSONRenderer]
    throttle_scope = 'register_login'

    def post(self, request):
        serializers = LoginSerializer(data= request.data)
        serializers.is_valid(raise_exception = True)

        email = serializers.validated_data['email']
        user = User.objects.get(email = email)
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({"status": "Login successful","access": access, "refresh": str(refresh)}, status=status.HTTP_200_OK)    

    
class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token: 
            raise ValidationError({"refresh": "This field is required."})
        
        try:
            refresh = RefreshToken(refresh_token)
            access = str(refresh.access_token)
            return Response({"access" : access}, status = status.HTTP_200_OK)
        
        except Exception:
            raise ValidationError({"detail" :"invalid or expired refresh token"})
        

class PasswordSetView(APIView):

    def post(self, request):
        serializer = PasswordSetSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']    
        user = User.objects.get(email = email)
        if user.has_usable_password():
            raise ValidationError({"detail": "Password is already set for this account."})
        else:
            user.set_password(password)
            user.save()
            return Response({"status": "Password set successfully"}, status = status.HTTP_200_OK)
        