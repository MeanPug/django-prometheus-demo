from django import forms
from walker import models


class StartWalkForm(forms.ModelForm):
    class Meta:
        model = models.Walk
        fields = ['dog', 'walker']
