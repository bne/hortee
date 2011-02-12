from django.conf import settings
from django import forms

from models import *

class PlotForm(forms.ModelForm):

    class Meta:
        model = Plot
        fields = ('name',)

class ActorForm(forms.ModelForm):
    
    def __init__(self, request, *args, **kwargs):
        """Only display plots owned by the user"""
        super(ActorForm, self).__init__(*args, **kwargs)
        self.fields['plot'].queryset = Plot.objects.filter(owners=request.user)
        self.fields['plot'].initial = request.session.get(
            settings.SESSION_KEY_DEFAULT_PLOT)
        
    class Meta:
        model = Actor
        fields = ('name', 'plot',)

class EventForm(forms.ModelForm):

    class Meta:
        model = Event

