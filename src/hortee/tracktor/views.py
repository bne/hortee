from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Plot, Actor, Event

@login_required
def _map(request):
    """View for plot map
    """
    return render_to_response('map.html', {
        }, context_instance=RequestContext(request))
        
@login_required
def _list(request):
    """View for actor list
    """
    actors = Actor.objects.filter(plot__owners=request.user).order_by('-id')
    return render_to_response('list.html', {
            'actors': actors,
        }, context_instance=RequestContext(request))        
        
@login_required
def add_actor(request):
    """View for adding an actor to a plot
    """
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
    """View for deleting an actor from a plot
    """
    id = None
    if request.method == 'POST':
        try:
            id = request.POST.get('id', None)
            Actor.objects.get(id=id).delete()
        except Actor.DoesNotExist:
            pass
    return HttpResponse(id) 

@login_required
def list_events(request, id=None):
    """View for listing events
    """
    events = Event.objects.filter(actor=id)
    return render_to_response('list-events.html', {
            'events': events,
        }, context_instance=RequestContext(request))
        
@login_required
def add_event(request):
    """View for adding an event to an actor
    """
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
    """View for deleting an event
    """
    id = None
    if request.method == 'POST':
        try:
            id = request.POST.get('id', None)
            Event.objects.get(id=id).delete()
        except Event.DoesNotExist:
            pass
    return HttpResponse(id) 

@login_required
def add_plot(request):
    """View for adding a plot
    """
    plots = request.session.get('plots', [])
    if request.method == 'POST':
        name = request.POST.get('name', None)
        if name:
            plot = Plot(name=name)
            plot.save()
            plot.owners.add(request.user)
            list(plots).append(plot)
            request.session['plots'] = plots
    return render_to_response('list-plots.html', {
            'plots': plots,
        }, context_instance=RequestContext(request))

@login_required
def delete_plot(request):
    """View for deleting a plot
    """
    id = None
    if request.method == 'POST':
        try:
            id = request.POST.get('id', None)
            Plot.objects.get(id=id).delete()
        except Plot.DoesNotExist:
            pass
    return HttpResponse(id) 
    
