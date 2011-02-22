from utils import SerializedApi
from resources import *

api = SerializedApi(api_name='api')
api.register(UserResource())
api.register(PlotResource())
api.register(ActorResource())
api.register(EventResource())

