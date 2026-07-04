from django.urls import path

# from .auth.views.register import views
from .auth.views.register import RegisterView
from .auth.views.otp import RegisterOTPSentView, RegisterOTPVerifyView, LoginOTPSendView, LoginOTPVerifyView
from .auth.views.login import LoginView, PasswordSetView

urlpatterns = [
    path('v1/register', RegisterView.as_view(), name='register'),
    path('v1/login', LoginView.as_view(), name='login'),
    path('v1/password-set', PasswordSetView.as_view(), name='password-set'),
    path('v1/register/otp-send',RegisterOTPSentView.as_view(), name='register-send_otp'),
    path('v1/register/otp-verify',RegisterOTPVerifyView.as_view(), name='register-verify_otp'),
    path('v1/login/otp-send', LoginOTPSendView.as_view(), name='login-send-otp'),
    path('v1/login/otp-verify', LoginOTPVerifyView.as_view(), name='login-verify-otp'),

    ]



