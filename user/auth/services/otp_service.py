import secrets
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError 


OTP_EXPIRY = 300  # 5 minutes

def generate_otp():
    return str(secrets.randbelow(900000) + 100000)


def save_otp(email, otp):
    key = f"otp_{email}"
    cache.set(key, {"otp": otp, "attempts" : 0}, timeout=OTP_EXPIRY)


def send_otp_email(email,otp):
    subject = "Your OTP Code"
    from_email = settings.EMAIL_HOST_USER
    text_content = f"Your OTP code is: {otp}. It will expire in 5 minutes."
    html_content = render_to_string("emails/otp_email.html", {'otp': otp})

    email_message = EmailMultiAlternatives(subject, text_content, from_email, to=[email])
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()


def verify_otp(email, otp):
    MAX_ATTEMPTS = 3
    key = f"otp_{email}"
    data = cache.get(key)

    if not data:
        raise ValidationError("OTP expired or not found")

    if data["attempts"] >= MAX_ATTEMPTS:
        cache.delete(key)
        raise ValidationError({"detail": "Too many attempts OTP is invalid. Request a new OTP."})
    
    if data["otp"] != otp:
        data["attempts"] += 1
        cache.set(key, data, timeout=OTP_EXPIRY)
        raise ValidationError("Invalid OTP")
    
    cache.delete(key)

    return True