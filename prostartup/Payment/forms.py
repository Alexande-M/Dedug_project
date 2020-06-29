from django import forms
from .models import Personalaccount

class PersonalaccountForm(forms.ModelForm):
    class Meta:
        model = Personalaccount
        fields = ('summ',)

#class RefaillForm(forms.Form):
 #   summ = forms.FloatField()
