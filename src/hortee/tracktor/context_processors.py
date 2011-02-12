from django.conf import settings

from models import Plot

def tracktor(request):
    rtn = {}
    if request.user.is_authenticated():
        rtn['default_plot'] = request.session.get(
            settings.SESSION_KEY_DEFAULT_PLOT)
    return rtn
    
    
