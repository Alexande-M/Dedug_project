from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'name': 'name',
            'placeholder' : 'Имя ползователя:',
            'type' : 'text'
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'name': 'email',
            'placeholder' : 'E-mail:',
            'type' : 'email',
        }
    ))
    subject = forms.CharField(widget=forms.TextInput(
        attrs={
            'name': 'subject',
            'placeholder' : 'Тема сообщения: ',
            'type' : 'text',
        }
    ))
    massage = forms.CharField(widget=forms.Textarea(
        attrs={
            'placeholder' : 'Ваш вопрос:',
            'maxlength' : '1000',
            'name' : 'coments', 
            'id' : 'coments',
        }
    ))