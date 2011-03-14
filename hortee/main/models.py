from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    """Additional user information
    """
    user = models.OneToOneField(User)
    settings = models.TextField(null=True, blank=True)
    
def create_user_profile(sender, instance, signal, created, *args, **kwargs):
    if created:
        profile = UserProfile(user=instance)
        profile.save()

post_save.connect(create_user_profile, sender=User, 
    dispatch_uid='hortee.main.create_user_profile')

