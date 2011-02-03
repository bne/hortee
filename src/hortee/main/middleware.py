from django.conf import settings

class UserAgentMiddleware(object):
    """Useful information about the user agent"""
    def process_request(self, request):
        setattr(request, 'device_type', 'mobile')
