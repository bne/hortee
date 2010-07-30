from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Plot, Actor

def list_actors(request):
    actors = None
    return render_to_response('list.html', {
        'actors': actors,
        }, context_instance=RequestContext(request))

