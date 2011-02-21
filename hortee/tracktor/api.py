from django.contrib.auth.models import User
from django.conf import settings

from tastypie.resources import ModelResource
from tastypie.api import Api
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

from models import *

class DjangoAuthentication(Authentication):
    """Checks is_authenticated on request.user as we're only going to be using 
    this Api on this domain following a client login
    """
    def is_authenticated(self, request, **kwargs):
        if hasattr(request, 'user') and request.user.is_authenticated():
            return True
        return False

    def get_identifier(self, request):
        return request.user.username

class UserResource(ModelResource):
    """Api resource for django.contrib.auth.models.User
    """
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'first_name', 'last_name']
        allowed_methods = ['get']     
        authentication = DjangoAuthentication()  

class PlotResource(ModelResource):
    """Api resource for tracktor.models.Plot
    """
    owners = fields.ManyToManyField(UserResource, 'owners')
    
    def get_object_list(self, request):
        """Restrict to Plots owned by user
        """
        object_list = self._meta.queryset
        return object_list.filter(owners=request.user)
    
    class Meta:
        queryset = Plot.objects.all()
        authentication = DjangoAuthentication()
        
class ActorResource(ModelResource):
    """Api resource for tracktor.models.Actor
    """
    plot = fields.ForeignKey(PlotResource, 'plot')
    
    def get_object_list(self, request):
        """Restrict to Plots owned by user
        """
        object_list = self._meta.queryset.filter(plot__owners=request.user)
        if not request.GET.get('plot'):
            plot = request.user.get_profile().get_default_plot()
            if plot:
                object_list = object_list.filter(plot=plot)
        return object_list

    class Meta:
        queryset = Actor.objects.all()
        authentication = DjangoAuthentication()
        filtering = {
            'plot': ('exact'),
        }
        
class EventResource(ModelResource):
    """Api resource for tracktor.models.Event
    """
    actor = fields.ForeignKey(ActorResource, 'actor')
    
    def get_object_list(self, request):
        """Restrict to Plots owned by user
        """
        object_list = self._meta.queryset
        return object_list.filter(actor__plot__owners=request.user)

    class Meta:
        queryset = Event.objects.all()
        authentication = DjangoAuthentication()
        filtering = {
            'actor': ('exact'),
        }


api = Api(api_name='api')
api.register(UserResource())
api.register(PlotResource())
api.register(ActorResource())
api.register(EventResource())

