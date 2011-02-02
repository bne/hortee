from models import Plot

def tracktor(request):
    rtn = {}
    if request.user.is_authenticated():
        rtn['plots'] = request.session.get('plots', None)
    return rtn
    
    
