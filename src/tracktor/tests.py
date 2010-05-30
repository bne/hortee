import time
from datetime import datetime

from django.test import TestCase
from tracktor.models import Actor

class EnvTest(TestCase):
    def testEnv(self):
        self.assert_(True)
        
class ActorTest(TestCase):
    def setUp(self):
        self.actor = Actor.objects.create(name="test_actor")
        
    def testCreate(self):
        self.assertEquals(self.actor.name, "test_actor")
        self.assertAlmostEqual(
            time.mktime(self.actor.start.timetuple()), 
            time.mktime(datetime.now().timetuple()))
        self.assertEquals(self.actor.end, None)
