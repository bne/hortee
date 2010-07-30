import time
from datetime import datetime

from django.test import TestCase
from models import *

class EnvTest(TestCase):
    def testEnv(self):
        self.assert_(True)
        
class ActorTest(TestCase):
    def testCreate(self):
        self.actor = Actor.objects.create(name="test_actor")
        self.assertEquals(self.actor.name, "test_actor")
        
class EventTest(TestCase):
    def setUp(self):
        self.actor = Actor.objects.create(name="test_actor")
        
    def testCreate(self):
        self.event = Event.objects.create(actor=self.actor, name="test_event")
        self.assertEquals(self.event.name, 'test_event')
        self.assertAlmostEqual(
            time.mktime(self.event.date.timetuple()), 
            time.mktime(datetime.now().timetuple()))
            
class TimelineTest(TestCase):
    def setUp(self):
        self.actor = Actor.objects.create(name="test_actor")
        Event.objects.create(actor=self.actor, name="test_event-1",
            date=datetime(2000, 2, 2, 2, 2, 2))
        Event.objects.create(actor=self.actor, name="test_event-2",
            date=datetime(2000, 1, 1, 1, 1, 1))
        Event.objects.create(actor=self.actor, name="test-event-3",
            date=datetime(2000, 5, 5, 5, 5, 5))
        Event.objects.create(actor=self.actor, name="test-event-4",
            date=datetime(2000, 4, 4, 4, 4, 4))        
        Event.objects.create(actor=self.actor, name="test-event-5",
            date=datetime(2000, 3, 3, 3, 3, 3))
        
    def testCreate(self):
        self.assertEquals(len(self.actor.get_timeline()), 5)
        
    def testStart(self):
        self.assertEquals(self.actor.date_start, datetime(2000, 1, 1, 1, 1, 1))
        
    def testEnd(self):
        self.assertEquals(self.actor.date_end, datetime(2000, 5, 5, 5, 5, 5))
        
    def testGetPeriod(self):
        self.assertEquals(len(self.actor.get_timeline(
            start=datetime(2000, 3, 3, 3, 3, 3),
            end=datetime(2000, 5, 5, 5, 5, 5)
        )), 3)        
        self.assertEquals(len(self.actor.get_timeline(
            start=datetime(2000, 2, 2, 2, 2, 2)
        )), 4)        
        self.assertEquals(len(self.actor.get_timeline(
            end=datetime(2000, 4, 4, 4, 4, 4)
        )), 4)
        
class EndEventTest(TestCase):
    def setUp(self):
        self.actor = Actor.objects.create(name="test_actor")
        self.start_event = Event.objects.create(actor=self.actor, 
            name="start_event",
            date=datetime(2000, 1, 1, 1, 1, 1))
            
    def testCreate(self):
        event = EndEvent.objects.create(
            actor=self.actor, name='test_event',
            start_event=self.start_event,
            date=datetime(2000, 2, 2, 2, 2, 2))            
        self.assertEquals(event.start_event, self.start_event)
                   
    def testDateValidation(self):
        # Start event date should be before object date
        self.assertRaises(ValidationError, EndEvent.objects.create,
            actor=self.actor, name='test_event',
            start_event=self.start_event,
            date=datetime(1999, 1, 1, 1, 1, 1))
            
    def testActorValidation(self):
        # Start date actor should be the same as object actor
        actor2 = Actor.objects.create(name='test_actor2')
        self.assertRaises(ValidationError, EndEvent.objects.create,
            actor=actor2, name='test_event',
            start_event=self.start_event,
            date=datetime(2000, 1, 1, 1, 1, 1))
            
class TextContentEventTest(TestCase):
    def setUp(self):
        self.actor = Actor.objects.create(name="test_actor")
        
    def testCreate(self):
        self.event = TextContentEvent.objects.create(
            actor=self.actor, 
            name="test_textevent",
            text_content="some descriptive text")
        self.assertEquals(self.event.name, 'test_textevent')
        self.assertEquals(self.event.text_content, 'some descriptive text')
        
    
        
