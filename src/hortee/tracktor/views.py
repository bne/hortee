from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Plot, Actor, Event

@login_required
def _map(request):
    return render_to_response('map.html', {
        }, context_instance=RequestContext(request))
        
@login_required
def _list(request):
    actors = Actor.objects.filter(plot__owners=request.user).order_by('-id')
    return render_to_response('list.html', {
            'actors': actors,
        }, context_instance=RequestContext(request))        
        
@login_required
def add_actor(request):
    actors = []
    if request.method == 'POST':
        name = request.POST.get('name', None)
        if name:
            plot = Plot.objects.get(owners=request.user)
            actor = Actor(name=name, plot=plot)
            actor.save()
            actors.append(actor)
    return render_to_response('list-actors.html', {
            'actors': actors,
        }, context_instance=RequestContext(request))

@login_required
def delete_actor(request):
    id = None
    if request.method == 'POST':
        try:
            id = request.POST.get('id', None)
            Actor.objects.get(id=id).delete()
        except Actor.DoesNotExist:
            pass
    return HttpResponse(id) 

@login_required
def add_event(request):
    events = []
    if request.method == 'POST':
        actor_id = request.POST.get('actor_id', None)
        text = request.POST.get('text', None)
        if text and actor_id:
            actor = Actor.objects.get(id=actor_id)
            event = Event(actor=actor, text=text)
            event.save()
            events.append(event)
    return render_to_response('list-events.html', {
            'events': events,
        }, context_instance=RequestContext(request))

@login_required
def delete_event(request):
    id = None
    if request.method == 'POST':
        try:
            id = request.POST.get('id', None)
            Event.objects.get(id=id).delete()
        except Event.DoesNotExist:
            pass
    return HttpResponse(id) 

@login_required
def list_events(request, id=None):
    events = Event.objects.filter(actor=id)
    return render_to_response('list-events.html', {
            'events': events,
        }, context_instance=RequestContext(request))
    
