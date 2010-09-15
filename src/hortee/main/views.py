from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response
from django.template import RequestContext

def default(request):
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')    
    form = AuthenticationForm(request)    
    request.session.set_test_cookie()    
    
    return render_to_response('default.html', {
        'form': form,
        REDIRECT_FIELD_NAME: redirect_to
    }, context_instance=RequestContext(request))

