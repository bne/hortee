from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Actor, Event

def list_actors(request):
    actors = Actor.objects.filter(plot__owners=request.user)
    return render_to_response('list.html', {
            'actors': actors,
        }, context_instance=RequestContext(request))

def list_events(request, id=None):
    json = serializers.serialize('json', Event.objects.filter(actor=id))
    return HttpResponse(json, mimetype='application/json')
    
