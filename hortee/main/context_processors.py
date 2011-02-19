from django.conf import settings

def page(request):
    return { 'base_template': 'base.html' }
    
def debug(request):
    return { 'DEBUG': settings.DEBUG }
    
