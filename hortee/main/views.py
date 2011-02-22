from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.views import login as django_login
from django.views.decorators.cache import never_cache
from django.conf import settings

@csrf_protect
@never_cache
def default(request):
    """Unauthenticated default view    
    Wraps django login view so we redirect to logged in page when authenticated
    """
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
        
    return django_login(request, template_name='default.html')
    
