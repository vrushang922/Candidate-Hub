from django.db import models
from user.models import User

class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name = 'profile')
    username = models.CharField(max_length = 255)
    phone = models.CharField(max_length = 15)
    avatar = models.ImageField(upload_to = 'avatars/', null = True, blank = True)
    skills = models.ManyToManyField("Skills", related_name = "candidate_profiles", blank = True)
    prefered_roles = models.ManyToManyField("Prefered_roles", related_name = "candidate_profiles", blank = True)


    def __str__(self):
        return self.username


class Skills(models.Model):
    name = models.CharField(max_length = 255, unique = True, null = False)
    
    def __str__(self):
        return self.name
    
class Prefered_roles(models.Model):
    name = models.CharField(max_length = 255, unique = True, null = False)

    def __str__(self):
        return self.name
    
