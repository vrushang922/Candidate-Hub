from rest_framework.routers import SimpleRouter
from django.urls import path, include
from .views import UserProfileViewSet


urlpatterns = []


router = SimpleRouter()
router.register(r'v1/user-profile', UserProfileViewSet, basename='user-profile')
urlpatterns += router.urls
