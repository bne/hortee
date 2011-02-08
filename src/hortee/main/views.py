from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.views import login as django_login
from django.views.decorators.cache import never_cache

from tracktor.models import Plot
from tracktor.views import actor_list

def default(request):
    """View for default
    """
    if request.user.is_authenticated():
        return actor_list(request)
        
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')    
    form = AuthenticationForm(request)    
    request.session.set_test_cookie()    
    
    return render_to_response('default.html', {
        'form': form,
        REDIRECT_FIELD_NAME: redirect_to
    }, context_instance=RequestContext(request))

@csrf_protect
@never_cache
def login(request):
    """Login view
    
    Wraps django login view so we can do a few things after log in 
    """
    login_result = django_login(request, template_name='user/login.html')
    if request.user.is_authenticated():
        # TODO: make this a setting/add to profile model
        request.session['current_plot'] = request.session['plots'][0]
        
    return login_result
