from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Plot, Actor, Event

def add_actor(request):
    actors = []
    if request.method == 'POST':
        name = request.POST.get('name', None)
        if name:
            # TODO: multiple plots per user (select from list and ut in session)
            plot = Plot.objects.get(owners=request.user)
            actor = Actor(name=name, plot=plot)
            actor.save()
            actors.append(actor)
    return render_to_response('list-actors.html', {
            'actors': actors,
        }, context_instance=RequestContext(request))

def list_actors(request):
    # TODO: multiple plots per user (select from list and ut in session)
    actors = Actor.objects.filter(plot__owners=request.user).order_by('-id')
    return render_to_response('list.html', {
            'actors': actors,
        }, context_instance=RequestContext(request))

def list_events(request, id=None):
    events = Event.objects.filter(actor=id)
    return render_to_response('list-events.html', {
            'events': events,
        }, context_instance=RequestContext(request))
    
