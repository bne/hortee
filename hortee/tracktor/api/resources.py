from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.defaults import url
from django.shortcuts import get_object_or_404

from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import Authorization
from utils import DjangoAuthentication as Authentication

from hortee.tracktor.models import *

class UserResource(ModelResource):
    """Api resource for django.contrib.auth.models.User
    """      
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'first_name', 'last_name']
        allowed_methods = ['get', 'put']
        authorization = Authorization()
        authentication = Authentication()  
        filtering = {
            'username': ('exact'),
        }
        
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<username>[\w\d_.-]+)/$" % \
                self._meta.resource_name, 
                self.wrap_view('dispatch_detail'), 
                name="api_dispatch_detail"),
        ]             

class PlotResource(ModelResource):
    """Api resource for tracktor.models.Plot
    """
    owners = fields.ManyToManyField(UserResource, 'owners')
    
    def get_object_list(self, request):
        """Restrict to Plots owned by user
        """
        object_list = self._meta.queryset
        if request and hasattr(request, 'user'):
            object_list = object_list.filter(owners=request.user)
        return object_list
    
    class Meta:
        queryset = Plot.objects.all()
        authorization = Authorization()
        authentication = Authentication()
        
class ActorResource(ModelResource):
    """Api resource for tracktor.models.Actor
    """
    plot = fields.ForeignKey(PlotResource, 'plot')
            
    def obj_create(self, *args, **kwargs):
        """Add logged in user as author
        """
        if kwargs.has_key('request'):
            kwargs['author'] = kwargs['request'].user
            return super(ActorResource, self).obj_create(*args, **kwargs)

    def obj_update(self, *args, **kwargs):
        """Add logged in user as author
        """
        if kwargs.has_key('request'):
            kwargs['author'] = kwargs['request'].user
            return super(ActorResource, self).obj_update(*args, **kwargs)

    def get_object_list(self, request):
        """Restrict to Plots owned by user
        """
        object_list = self._meta.queryset
        if request and hasattr(request, 'user'):
            object_list = object_list.filter(plot__owners=request.user)
        return object_list
            
    class Meta:
        queryset = Actor.objects.all()
        authorization = Authorization()
        authentication = Authentication()
        filtering = {
            'plot': ('exact'),
        }
        
class ActionResource(ModelResource):
    """Api resource for tracktor.models.Action
    """
    actor = fields.ForeignKey(ActorResource, 'actor')
        
    def obj_create(self, *args, **kwargs):
        """Add logged in user as author
        """
        if kwargs.has_key('request'):
            kwargs['author'] = kwargs['request'].user
            return super(ActionResource, self).obj_create(*args, **kwargs)

    def obj_update(self, *args, **kwargs):
        """Add logged in user as author
        """
        if kwargs.has_key('request'):
            kwargs['author'] = kwargs['request'].user
            return super(ActionResource, self).obj_update(*args, **kwargs)
    
    def get_object_list(self, request):
        """Restrict to Plots owned by user
        """
        object_list = self._meta.queryset
        return object_list.filter(actor__plot__owners=request.user)

    class Meta:
        queryset = Action.objects.all()
        authorization = Authorization()
        authentication = Authentication()
        
        filtering = {
            'actor': ('exact'),
        }


