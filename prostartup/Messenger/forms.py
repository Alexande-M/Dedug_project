from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}
        widgets = {
            'message' : forms.Textarea(attrs={'placeholder' : 'Введите ваше сообщение', '': ''}),
        }