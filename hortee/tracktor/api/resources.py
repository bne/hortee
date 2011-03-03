from django.contrib.auth.models import User
from django.conf import settings

from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import Authorization
from utils import DjangoAuthentication

from hortee.tracktor.models import *

class UserResource(ModelResource):
    """Api resource for django.contrib.auth.models.User
    """
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'first_name', 'last_name']
        allowed_methods = ['get']     
        authorization = Authorization()
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
        authorization = Authorization()
        authentication = DjangoAuthentication()
        
class ActorResource(ModelResource):
    """Api resource for tracktor.models.Actor
    """
    plot = fields.ForeignKey(PlotResource, 'plot')
    
    def get_object_list(self, request):
        """Restrict to Plots owned by user
        """
        object_list = self._meta.queryset
        if request and hasattr(request, 'user'):
            object_list = object_list.filter(plot__owners=request.user)
            if not request.GET.get('plot'):
                plot = request.user.get_profile().get_default_plot()
                if plot:
                    object_list = object_list.filter(plot=plot)
        return object_list

    class Meta:
        queryset = Actor.objects.all()
        authorization = Authorization()
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
        authorization = Authorization()
        authentication = DjangoAuthentication()
        filtering = {
            'actor': ('exact'),
        }


