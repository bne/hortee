from datetime import datetime

from django.db import models

class Actor(models.Model):
    """A thing unto which things happen
    """
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name    
    
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
        If start and end are None, returns all events
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
    
    Not set as abstract in the meta class, so we can do Event.objects.get() for
    all models inheriting this one
    """
    actor = models.ForeignKey(Actor)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.now)
        
    def __unicode__(self):
        return self.name  
    
    class Meta:
        ordering = ["date"]
        
class TextContentEvent(Event):
    """Event with a descriptive text field
    """
    text_content = models.TextField()
    





