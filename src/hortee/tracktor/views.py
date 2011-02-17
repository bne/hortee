from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings

from models import *
from forms import *

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
        form = PlotForm(data=request.POST)
        if form.is_valid():
            plot = form.save()
            plot.owners.add(request.user)
            request.session[settings.SESSION_KEY_DEFAULT_PLOT] = plot
            messages.success(request, 'Plot added')
            return redirect('tracktor-plots')
    else:
        form = PlotForm()
    
    return render_to_response('tracktor/plot-add.html', {
        'form': form,
    }, context_instance=RequestContext(request))  
    
@login_required
def plot_set(request, id=None):
    """View for editing a plot
    """
    try:
        plot = Plot.objects.get(id=id)
        request.user.get_profile().default_plot = plot
        request.user.get_profile().save()
        request.session[settings.SESSION_KEY_DEFAULT_PLOT] = plot
        messages.success(request, 'Current plot set to %s' % (plot.name,))
    except Plot.DoesNotExist:
        messages.error(request, 'Plot not found')
        return redirect('tracktor-plots')
    
    return redirect('tracktor-actors')

@login_required
def plot_edit(request, id=None):
    """View for editing a plot
    """
    try:
        plot = Plot.objects.get(id=id)            
    except Plot.DoesNotExist:
        messages.error(request, 'Plot not found')
        return redirect('tracktor-plots')
        
    if request.method == 'POST':
        form = PlotForm(data=request.POST, instance=plot)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plot updated')
            return redirect('tracktor-plots')
    else:
        form = PlotForm(instance=plot)
        
    return render_to_response('tracktor/plot-edit.html', {
        'plot': plot,
        'form': form,
    }, context_instance=RequestContext(request))     

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
        plot=request.session.get(
            settings.SESSION_KEY_DEFAULT_PLOT)).order_by('-id')
    return render_to_response('tracktor/actors.html', {
            'actors': actors,
        }, context_instance=RequestContext(request))        
        
@login_required
def actor_add(request):
    """View for adding an actor to a plot
    """
    if request.method == 'POST':
        form = ActorForm(request, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Actor added')
            return redirect('tracktor-actors')
    else:
        form = ActorForm(request)
            
    return render_to_response('tracktor/actor-add.html', {
        'plots': Plot.objects.filter(owners=request.user),
        'form': form,
    }, context_instance=RequestContext(request))
        
@login_required
def actor_edit(request, id=None):
    """View for editing an actor
    """
    try:
        actor = Actor.objects.get(id=id)            
    except Actor.DoesNotExist:
        messages.error(request, 'Actor not found')
        return redirect('tracktor-actors')
        
    if request.method == 'POST':
        form = ActorForm(request, data=request.POST, instance=actor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Actor updated')
            return redirect('tracktor-actors')
    else:
        form = ActorForm(request, instance=actor)
            
    return render_to_response('tracktor/actor-edit.html', {
        'actor': actor,
        'form': form,
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
    try:
        actor = Actor.objects.get(id=actor_id)
    except Actor.DoesNotExist:
        messages.error(request, 'Actor not found')
        return redirect('tracktor-actors')    
    
    if request.method == 'POST':
        data = request.POST.copy()
        data['actor'] = actor.id
        form = EventForm(data=data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event added')
            return redirect('tracktor-events', actor_id=actor_id)
    else:
        form = EventForm(initial={ 'date': datetime.utcnow() })
        
    return render_to_response('tracktor/event-add.html', {
        'actor': actor,
        'form': form,
    }, context_instance=RequestContext(request))

@login_required
def event_edit(request, id=None):
    """View for editing an event
    """
    try:
        event = Event.objects.get(id=id)
    except event.DoesNotExist:
        messages.error(request, 'Event not found')
        return redirect('tracktor-actors')
        
    if request.method == 'POST':
        data = request.POST.copy()
        data['actor'] = event.actor.id
        form = EventForm(data=data, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated')
            return redirect('tracktor-events', actor_id=event.actor.id)
    else:
        form = EventForm(instance=event)
        
    return render_to_response('tracktor/event-edit.html', {
        'event': event,
        'form': form,
    }, context_instance=RequestContext(request))
        
@login_required
def event_delete(request, id=None):
    """View for deleting an event
    """
    try:
        event = Event.objects.get(id=id)
    except event.DoesNotExist:
        messages.error(request, 'Event not found')
        return redirect('tracktor-actors')
            
    if request.method == 'POST' and event:
        event.delete()
        messages.success(request, 'Event deleted')
        return redirect('tracktor-events', actor_id=event.actor.id)
        
    return render_to_response('tracktor/event-delete.html', {
        'event': event,
    }, context_instance=RequestContext(request))
        

