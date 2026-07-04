from rest_framework import serializers
from .models import CandidateProfile, Skills, Prefered_roles
from rest_framework.exceptions import ValidationError


class UserProfileViewSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source = "user.email")
    skills = serializers.SlugRelatedField(read_only = True, many = True, slug_field = "name")
    prefered_roles = serializers.SlugRelatedField(many = True,read_only = True, slug_field = "name")


    class Meta: 
        model = CandidateProfile
        fields = ["user", "username", "phone", "avatar", "skills", "prefered_roles"]


    def validate_phone(self, value):
        if not value.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        if len(value) < 10 or len(value) > 12:
            raise ValidationError("Phone number must be between 10 and 12 digits.")
        return value
    
    
