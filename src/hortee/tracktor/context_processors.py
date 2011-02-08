from models import Plot

def tracktor(request):
    rtn = {}
    if request.user.is_authenticated():
        rtn['current_plot'] = request.session.get('current_plot')
    return rtn
    
    
