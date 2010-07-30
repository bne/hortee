from django.shortcuts import render_to_response
from django.template import RequestContext

def default(request):
    return render_to_response('default.html', 
        context_instance=RequestContext(request))
        
def list_actors(request):
    actors = None
    return render_to_response('list.html', {
        'actors': actors,
        }, context_instance=RequestContext(request))
    


