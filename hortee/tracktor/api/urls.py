from utils import SerializedApi
from resources import *

api = SerializedApi(api_name='v1')
api.register(UserResource())
api.register(PlotResource())
api.register(ActorResource())
api.register(ActionResource())

urlpatterns = api.urls
