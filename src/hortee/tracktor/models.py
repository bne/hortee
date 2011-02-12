from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Plot(models.Model):
    """A pot into which to put Actors
    """
    # TODO: Geo coords fields
    name = models.CharField(max_length=100)
    owners = models.ManyToManyField(User)
    
    @staticmethod
    def get_default_plot(owner):
        """Works out the default plot for the given owner
        """
        _plot = owner.get_profile().default_plot
        if not _plot:
            _plot = Plot.objects.filter(owners=owner)[:0]
            if _plot:
                return _plot[0]

        return _plot
    
    def __unicode__(self):
        return self.name

class Actor(models.Model):
    """A thing unto which things happen
    """
    name = models.CharField(max_length=100)
    plot = models.ForeignKey(Plot)
    
    def __unicode__(self):
        return self.name    
    
    @property
    def date_start(self):
        return Event.objects.order_by('date')[0].date
        
    @property
    def date_end(self):
        return Event.objects.order_by('-date')[0].date
                
class Event(models.Model):
    """An event on the actor's timeline
    """
    actor = models.ForeignKey(Actor)
    text = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
        
    def __unicode__(self):
        return self.text  
    
    class Meta:
        ordering = ["date"]

