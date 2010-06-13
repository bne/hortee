from datetime import datetime

from django.db import models

class Actor(models.Model):
    """A thing unto which things happen
    """
    name = models.CharField(max_length=100)
    
    @property
    def date_start(self):
        return Event.objects.order_by('date')[0].date
        
    @property
    def date_end(self):
        return Event.objects.order_by('-date')[0].date
        
    def get_timeline(self, start=None, end=None):
        """Returns the events between 2 dates for this Actor
        If start is None, returns all Events up to end
        If end is None returns all Events after start
        If start and end are None, returns all events for this Actor
        """
        if not start is None and not end is None:
            return Event.objects.filter(actor=self, 
                date__gte=start, date__lte=end)
        elif start is None and not end is None:
            return Event.objects.filter(actor=self, date__lte=end)
        elif not start is None and end is None:
            return Event.objects.filter(actor=self, date__gte=start)
        return  Event.objects.filter(actor=self)
    
class Event(models.Model):
    """Base class for all events on the timeline
    """
    actor = models.ForeignKey(Actor)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.now)
    
    class Meta:
        ordering = ["date"]
    





