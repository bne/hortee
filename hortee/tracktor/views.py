from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from api.urls import api
from api.resources import PlotResource

@login_required
def actors(request):
    """Main list view
    """
    plot_resource = PlotResource()
    
    return render_to_response('tracktor/list.html', {
        'api_disco': api.serialized(request, desired_format='application/json'),
        'default_plot': request.user.get_profile().get_default_plot(),
    }, context_instance=RequestContext(request))


