from django.shortcuts import render_to_response
from django.template import RequestContext

def default(request):
    """default
    """
    return render_to_response('default.html', {
    }, context_instance=RequestContext(request))

