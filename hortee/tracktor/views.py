from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from api.urls import api

@login_required
def list_(request):
    """Main list view
    """
    return render_to_response('tracktor/list.html', {
        'api_disco': api.serialized(request, desired_format='application/json'),
    }, context_instance=RequestContext(request))


