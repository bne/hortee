from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Plot(models.Model):
    """A pot into which to put Actors
    """
    name = models.CharField(max_length=100)
    owners = models.ManyToManyField(User)
    lng = models.DecimalField(
        max_digits=12, decimal_places=9, blank=True, null=True,
        verbose_name='Longitude')
    lat = models.DecimalField(
        max_digits=12, decimal_places=9, blank=True, null=True, 
        verbose_name='Latitude')
        
    def __unicode__(self):
        return self.name

class Actor(models.Model):
    """A thing unto which things happen
    """
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    plot = models.ForeignKey(Plot)
    
    def __unicode__(self):
        return self.name
    
    @property
    def date_start(self):
        return Action.objects.order_by('date')[0].date
        
    @property
    def date_end(self):
        return Action.objects.order_by('-date')[0].date
                
class Action(models.Model):
    """An action on the actor's timeline
    """
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    actor = models.ForeignKey(Actor)
    text = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=datetime.now)
            
    def __unicode__(self):
        return self.text  
    
    class Meta:
        ordering = ["date"]

