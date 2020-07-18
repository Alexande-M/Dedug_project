from django import forms
from django.contrib.auth.models import User
from .models import Profile, Subscription
from ProjectManager.models import Project


class UpgradeProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ('project_name', 'category','presentation','project_img_one','project_img_two','project_img_three','full_project_description', 'business_plan', 'project_cost', 'project_investment',)
        
        widgets = {
            'project_name'       : forms.TextInput(attrs={'placeholder' : 'Главный заголовок проекта'}),
            'choices'            : forms.Select(attrs={'id': 'type', 'name' : 'type'}),
            'presentation'       : forms.Textarea(attrs={'placeholder' : 'Краткое описание проекта', 'maxlength': '1000'}),
            'project_investment' : forms.TextInput(attrs={'placeholder' : 'Стоимость инвестиции','id':'', '' : ''}),
            'business_plan'            : forms.FileInput(attrs={'type': 'file','name':'business_plan', 'id': 'plan'}),
            'full_project_description' : forms.FileInput(attrs={'type': 'file','name':'full_project_description', 'id': 'presentation'}),
            'project_img_one'    : forms.FileInput(attrs={'type': 'file', 'id' : 'add-img1', 'accept' : 'image/*'}),
            'project_img_two'    : forms.FileInput(attrs={'type': 'file', 'id' : 'add-img2', 'accept' : 'image/*'}),
            'project_img_three'  : forms.FileInput(attrs={'type': 'file', 'id' : 'add-img3', 'accept' : 'image/*'}),
        }


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('project_name', 'category','presentation','project_img_one','project_img_two','project_img_three','choices','full_project_description', 'business_plan', 'project_cost', 'project_investment',)
        widgets = {
            'project_name'       : forms.TextInput(attrs={'placeholder' : 'Главный заголовок проекта'}),
            'choices'            : forms.Select(attrs={'id': 'type', 'name' : 'type'}),
            'presentation'       : forms.Textarea(attrs={'placeholder' : 'Краткое описание проекта', 'maxlength': '1000'}),
            'project_cost'       : forms.TextInput(attrs={'placeholder' : 'Стоимость проекта в USD'}),
            'project_investment' : forms.TextInput(attrs={'placeholder' : 'Стоимость инвестиции','id':'investCost', 'disabled' : 'disabled'}),
            'business_plan'      : forms.FileInput(attrs={'type': 'file','name':'business_plan', 'id': 'plan'}),
            'full_project_description' : forms.FileInput(attrs={'type': 'file','name':'full_project_description', 'id': 'presentation'}),
            'project_img_one'    : forms.FileInput(attrs={'type': 'file', 'id' : 'add-img1', 'accept' : 'image/*'}),
            'project_img_two'    : forms.FileInput(attrs={'type': 'file', 'id' : 'add-img2', 'accept' : 'image/*'}),
            'project_img_three'  : forms.FileInput(attrs={'type': 'file', 'id' : 'add-img3', 'accept' : 'image/*'}),
        }
        

class RefaillForm(forms.Form):
    summ = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder' : 'Введите сумму'}))


class SubscriptionFormData(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ('cost',)
        widgets = {
            'cost': forms.Select(attrs={'id': 'subscriptionInv'}),
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'phone', 'hide_personal_data')
        widgets = {
            'phone': forms.TextInput(attrs={'class': '', 'placeholder' : 'Телефон'}),
            'photo': forms.FileInput(attrs={'type': 'file', 'id' : 'profile-image', 'accept' : 'image/*','name' : 'profile-image' ,}),
            'hide_personal_data' : forms.CheckboxInput(attrs={'id': 'private-data','type' : 'checkbox','name':'private-data'}),
        }

class UserEditForm(forms.ModelForm):
    old_pass = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Старый пароль'}),required=False)
    new_pass = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Новый пароль'}),required=False)
    new_pass_rep = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Подтвердите новый пароль'}),required=False)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': '', 'placeholder' : 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': '', 'placeholder' : 'Фамилия'}),
            'email': forms.TextInput(attrs={'class': '', 'placeholder' : 'E-mail'}),
        }



class UserRegistrationForm(forms.ModelForm):

    password_one = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'myclass',
            'placeholder' : 'Пароль',
        }
    ))
    password_two = forms.CharField(label='Repeat password', widget=forms.PasswordInput(
        attrs={
            'class': 'myclass',
            'placeholder' : 'Подтверждение пароля',
        }
    ))
    check_polity = forms.BooleanField(required=True,widget=forms.CheckboxInput(
            attrs={
                'id': 'check',
                'type' : 'checkbox'
            }
        ))
    # chek_polity = forms.MultipleChoiceField(required=False,)
    
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email',) 
        widgets = {
            'username': forms.TextInput(attrs={'class': 'myclass', 'placeholder' : 'Имя пользователя на сайте'}),
            'first_name': forms.TextInput(attrs={'class': 'myclass', 'placeholder' : 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'myclass', 'placeholder' : 'Фамилия'}),
            'email': forms.TextInput(attrs={'class': 'myclass', 'placeholder':'E-mail'}),
        }
        
    def clean_password_two(self):
        cd = self.cleaned_data
        if cd['password_one'] != cd['password_two']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password_two']








