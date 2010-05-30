from django.db import models

class Actor(models.Model):
    """An item to which things happen
    """
    name = models.CharField(max_length=100)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True)
