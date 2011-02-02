from models import Plot

def tracktor(request):
    rtn = {}
    if request.user.is_authenticated():
        rtn['plots'] = Plot.objects.filter(owners=request.user)
    return rtn
    
    
