from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse

from models import Plot, Actor, Event

@login_required
def plot_map(request):
    """View for plot map
    """
    return render_to_response('tracktor/map.html', {
    }, context_instance=RequestContext(request))

## ============================================================================
## Plots
## ============================================================================
       
@login_required
def plot_list(request):
    """Manage plot settings   
    """    
    plots = Plot.objects.filter(owners=request.user)    
    return render_to_response('tracktor/plots.html', {
        'plots': plots,
    }, context_instance=RequestContext(request))
    
@login_required
def plot_add(request):
    """View for adding a new plot
    """
    if request.method == 'POST':
        name = request.POST.get('plot_name')
        if name:
            plot = Plot(name=name)
            plot.save()
            plot.owners.add(request.user)
            messages.success(request, 'Plot added')

        return redirect('tracktor-plots')
        
    return render_to_response('tracktor/plot-add.html', {
    }, context_instance=RequestContext(request))  

@login_required
def plot_edit(request, id=None):
    """View for editing a plot
    """
    return id

@login_required
def plot_delete(request, id=None):
    """View for deleting a plot
    """
    try:
        plot = Plot.objects.get(id=id)            
    except Plot.DoesNotExist:
        messages.error(request, 'Plot not found')
        return redirect('tracktor-plots')
            
    if request.method == 'POST' and plot:
        plot.delete()
        messages.success(request, 'Plot %s deleted' % (plot.name,))
        return redirect('tracktor-plots')
        
    return render_to_response('tracktor/plot-delete.html', {
        'plot': plot,
    }, context_instance=RequestContext(request))
        
## ============================================================================
## Actors
## ============================================================================        
        
@login_required
def actor_list(request):
    """View for actor list
    """
    actors = Actor.objects.filter(
        plot__owners=request.user,
        plot=request.session.get('current_plot')).order_by('-id')
    return render_to_response('tracktor/actors.html', {
            'actors': actors,
        }, context_instance=RequestContext(request))        
        
@login_required
def actor_add(request):
    """View for adding an actor to a plot
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            plot = request.POST.get('plot')
            actor = Actor(name=name, plot=plot)
            actor.save()
            messages.success(request, 'Actor added')
            
        return redirect('tracktor-actors')
            
    return render_to_response('tracktor/actor-add.html', {
        'plots': Plot.objects.filter(owners=request.user),
    }, context_instance=RequestContext(request))

@login_required
def actor_delete(request, id=None):
    """View for deleting an actor from a plot
    """
    try:
        actor = Actor.objects.get(id=id)            
    except Actor.DoesNotExist:
        messages.error(request, 'Actor not found')
        return redirect('tracktor-actors')
            
    if request.method == 'POST' and actor:
        actor.delete()
        messages.success(request, 'Actor deleted')
        return redirect('tracktor-actors')
        
    return render_to_response('tracktor/actor-delete.html', {
        'actor': actor,
    }, context_instance=RequestContext(request))
        
## ============================================================================
## Events
## ============================================================================
        
@login_required
def event_list(request, actor_id=None):
    """View for listing events
    """
    try:
        actor = Actor.objects.get(id=actor_id)
    except Actor.DoesNotExist:
        messages.error(request, 'Actor not found')
        return redirect('tracktor-actors')
            
    return render_to_response('tracktor/events.html', {
        'events': actor.event_set.all(),
        'actor': actor,
    }, context_instance=RequestContext(request))

@login_required
def event_add(request, actor_id=None):
    """View for adding an event to an actor
    """
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            try:
                date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d')
            except:
                date = datetime.utcnow()
            actor = Actor.objects.get(pk=actor_id)
            event = Event(actor=actor, text=text, date=date)
            event.save()
            messages.success(request, 'Event added')
            
        return redirect('tracktor-events', actor_id=actor_id)
        
    return render_to_response('tracktor/event-add.html', {
        'actor_id': actor_id,
    }, context_instance=RequestContext(request))

@login_required
def event_edit(request):
    """View for editing an event
    """
    return render_to_response('tracktor/event-add.html', {
    }, context_instance=RequestContext(request))
        
@login_required
def event_delete(request, id=None):
    """View for deleting an event
    """
    actor_id = None
    try:
        event = Event.objects.get(id=id)
        actor_id = event.actor.id            
    except event.DoesNotExist:
        messages.error(request, 'Event not found')
        return redirect('tracktor-actors')
            
    if request.method == 'POST' and event:
        event.delete()
        messages.success(request, 'Event deleted')
        return redirect('tracktor-events', actor_id=actor_id)
        
    return render_to_response('tracktor/event-delete.html', {
        'event': event,
    }, context_instance=RequestContext(request))
        

