from django.conf import settings

def page(request):
    template_dir = '%s/' % (request.device_type,) if request.device_type else ''
    return { 'base_template': '%sbase.html' % (template_dir,) }
    
def debug(request):
    return { 'DEBUG': settings.DEBUG }
    
