from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from hortee.tracktor.models import Plot

class UserProfile(models.Model):
    """Additional user information
    """
    user = models.OneToOneField(User)
    settings = models.TextField(null=True, blank=True)
    default_plot = models.ForeignKey(Plot, null=True)
    
    def get_default_plot(self):
        """Works out the default plot for this user
        """
        if not self.default_plot:
            plots = Plot.objects.filter(owners=self.user)
            if plots:
                self.default_plot = plots[0]
                self.save()
            
        return self.default_plot
    
def create_user_profile(sender, instance, signal, created, *args, **kwargs):
    if created:
        profile = UserProfile(user=instance)
        profile.save()

post_save.connect(create_user_profile, sender=User, 
    dispatch_uid='hortee.main.create_user_profile')

