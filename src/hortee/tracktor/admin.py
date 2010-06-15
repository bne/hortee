from django.contrib import admin
from models import Actor, Event

class ActorAdmin(admin.ModelAdmin):
    list_display = ('name')
    
admin.site.register(Actor)

class EventAdmin(admin.ModelAdmin):
    list_display = ('name')
    
admin.site.register(Event)
