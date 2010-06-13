from datetime import datetime

from django.db import models

class Actor(models.Model):
    """An item to which things happen
    """
    name = models.CharField(max_length=100)
    
    @property
    def events(self):
        return Event.objects.filter(actor=self)
        
    @property
    def date_start(self):
        return Event.objects.order_by('date')[0].date
        
    @property
    def date_end(self):
        return Event.objects.order_by('-date')[0].date
        
class Event(models.Model):
    """Base class for all events on the timeline
    """
    actor = models.ForeignKey(Actor)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.now)
    
    class Meta:
        ordering = ["date"]
    





