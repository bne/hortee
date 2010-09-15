from models import Plot

def tracktor(request):
    plots = Plot.objects.filter(owners=request.user)
    return { 'plots': plots }
    
    
