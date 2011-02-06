from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from models import Plot, Actor, Event

@login_required
def plot_map(request):
    """View for plot map
    """
    return render_to_response('tracktor/map.html', {
    }, context_instance=RequestContext(request))
        
@login_required
def list_actors(request):
    """View for actor list
    """
    actors = Actor.objects.filter(
        plot__owners=request.user,
        plot=request.session.get('current_plot')).order_by('-id')
    return render_to_response('tracktor/actors.html', {
            'actors': actors,
        }, context_instance=RequestContext(request))        
        
@login_required
def add_actor(request):
    """View for adding an actor to a plot
    """
    if request.method == 'POST':
        name = request.POST.get('actor_name', None)
        if name:
            plot = request.session.get('current_plot')
            actor = Actor(name=name, plot=plot)
            actor.save()            
        return redirect('main-default')
            
    return render_to_response('tracktor/actor-add.html', {}, 
        context_instance=RequestContext(request))

@login_required
def delete_actor(request, id=None):
    """View for deleting an actor from a plot
    """
    if request.method == 'POST':
        try:
            Actor.objects.get(id=id).delete()
        except Actor.DoesNotExist:
            pass
    return HttpResponse(id) 

@login_required
def list_events(request, id=None):
    """View for listing events
    """
    events = Event.objects.filter(actor=id)
    return render_to_response('tracktor/events.html', {
        'events': events,
        'actor_id': id,
    }, context_instance=RequestContext(request))

@login_required
def add_event(request, id=None):
    """View for adding an event to an actor
    """
    if request.method == 'POST':
        text = request.POST.get('event_text')
        if text:
            actor = Actor.objects.get(id=id)
            event = Event(actor=actor, text=text)
            event.save()
            
        return redirect('tracktor-events', id=id)
        
    return render_to_response('tracktor/event-add.html', {
        'actor_id': id,
    }, context_instance=RequestContext(request))

@login_required
def edit_event(request):
    """View for editing an event
    """
    return render_to_response('tracktor/event-add.html', {
    }, context_instance=RequestContext(request))
    
    
@login_required
def delete_event(request, id=None):
    """View for deleting an event
    """
    if request.method == 'POST':
        try:
            Event.objects.get(id=id).delete()
        except Event.DoesNotExist:
            pass
    return HttpResponse(id)
    
@login_required
def plots(request):
    """Manage plot settings
    """
    if request.method == 'POST':
        name = request.POST.get('plot_name')
        plot = None
        if name:
            plot = Plot(name=name)
            plot.save()
            plot.owners.add(request.user)
        else:
            try:
                plot = Plot.objects.get(id=request.POST.get('current_plot'))
            except Plot.DoesNotExist:
                pass
                
        request.session['current_plot'] = plot
        return redirect('main-default')
    
    plots = Plot.objects.filter(owners=request.user)    
    return render_to_response('tracktor/plots.html', {
        'plots': plots,
    }, context_instance=RequestContext(request))

@login_required
def delete_plot(request, id=None):
    """View for deleting a plot
    """
    if request.method == 'POST':
        try:
            Plot.objects.get(id=id).delete()
        except Plot.DoesNotExist:
            pass
    return HttpResponse(id) 
    
