from rest_framework.viewsets import ModelViewSet
from .serializers import UserProfileViewSerializer
from .models import CandidateProfile

class UserProfileViewSet(ModelViewSet):
    queryset = CandidateProfile.objects.all()
    serializer_class = UserProfileViewSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CandidateProfile.objects.all()
        user = self.request.user
        return CandidateProfile.objects.filter(user=user) 

    # def get_serializer_class(self):
    #     if self.request.method == "GET":
    #         return self.serializer_class
        
        # return UserProfileCreateSerializer

    
    def perform_create(self, serializer):
        serializer.save(user= self.request.user)
        
