from django import template
from django.contrib.auth.models import Group
from ..models import Profile,Notifications
from Messenger.models import Message
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
    if user:
        data_profile = Profile.objects.get(user = user) 
    else:
        return False
    return  data_profile.photo.url



@register.filter(name='notifications')
def notifications_data(user):
    try:
        if user:
            data_notifications = Notifications.objects.all().filter(user = user,is_readed=False) 
        else:
            return False
    except:
        data_notifications = None
        pass 
    return  data_notifications


@register.filter(name='count_message')
def count_message(user):
    count_is_readed = Message.objects.values_list('message',flat=True).filter(author = user, is_readed = False).count()
    return count_is_readed