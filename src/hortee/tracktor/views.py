from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Actor

def list_actors(request):
    actors = Actor.objects.filter(plot__owners=request.user)
    return render_to_response('list.html', {
        'actors': actors,
        }, context_instance=RequestContext(request))

