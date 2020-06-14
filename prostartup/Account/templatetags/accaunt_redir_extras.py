from django import template
from django.contrib.auth.models import Group
from ..models import Profile

register = template.Library()

@register.filter(name='has_group') 
def has_group(user, group_name): 
    try: 
        group = Group.objects.get(name=group_name) 
    except Group.DoesNotExist: 
        return False
    return group in user.groups.all() 


@register.filter(name='personal_data')
def personal_data(user):
    data_profile = Profile.objects.get(user = user) 
    return  data_profile.photo.url