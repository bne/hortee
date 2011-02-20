from tastypie.resources import ModelResource
from tastypie.api import Api
from models import *

class PlotResource(ModelResource):
    class Meta:
        queryset = Plot.objects.all()
        
class ActorResource(ModelResource):
    class Meta:
        queryset = Actor.objects.all()
        
class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()

def url_patterns():
    _api = Api(api_name='tracktor')
    _api.register(PlotResource())
    _api.register(ActorResource())
    _api.register(EventResource())
    return _api.urls

