from tastypie.api import Api
from tastypie.authentication import Authentication
from tastypie.serializers import Serializer
from tastypie.utils.mime import determine_format

class DjangoAuthentication(Authentication):
    """Checks is_authenticated on request.user as we're only going to be using 
    this Api on this domain following a client login
    """
    def is_authenticated(self, request, **kwargs):
        if hasattr(request, 'user') and request.user.is_authenticated():
            return True
        return False

    def get_identifier(self, request):
        return request.user.username
        
class SerializedApi(Api):
    def serialized(self, request, api_name=None, desired_format=None):
        """
        Nabbed from top_level of the parent class
        Would be nice if this was abstracted as it's good for auto discovery
        """
        serializer = Serializer()
        available_resources = {}
        
        if api_name is None:
            api_name = self.api_name
            
        if desired_format is None:
            desired_format = determine_format(request, serializer)
        
        for name in sorted(self._registry.keys()):
            available_resources[name] = {
                'list_endpoint': self._build_reverse_url("api_dispatch_list", kwargs={
                    'api_name': api_name,
                    'resource_name': name,
                }),
                'schema': self._build_reverse_url("api_get_schema", kwargs={
                    'api_name': api_name,
                    'resource_name': name,
                }),
            }
        
        return serializer.serialize(available_resources, desired_format)

