from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Additional user information
    """
    user = models.OneToOneField(User)
    settings = models.TextField(null=True, blank=True)
    
