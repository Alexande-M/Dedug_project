from django import forms
from .models import Project


class FavoriteAddProjectForm(forms.Form):
    ids = forms.IntegerField(required=False,initial=False,widget=forms.HiddenInput)
    update = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)

# class ProjectCreateForm(forms.ModelForm):
#     def clean_fields(self):
#         cd = self.cleaned_data
#         return cd


#     class Meta:
#         model = Project
#         fields = ('project_name', 'slug', 'category','presentation','full_project_description', 'business_plan', 'project_cost', 'project_investment','status_active_of_project')



        