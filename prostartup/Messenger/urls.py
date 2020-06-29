from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth.decorators import login_required


app_name = 'Messenger'

urlpatterns = [
    url(r'^dialogs/$', login_required(views.DialogsView.as_view()), name='dialogs'),
    url(r'^dialogs/create/(?P<user_id>\d+)/$', login_required(views.CreateDialogView.as_view()), name='create_dialog'),
    url(r'^dialogs/(?P<chat_id>\d+)/$', login_required(views.MessagesView.as_view()), name='messages'),
    url(r'^dialogs/(?P<chat_id>\d+)/remove/$', login_required(views.Clear_ChatView.as_view()), name='clear_chatView'),

    url(r'^dialogs/all_from_json/(?P<chat_id>\d+)/$', login_required(views.filter), name='all_from_json'),
    # url(r'^dialogs/(?P<chat_id>\d+)/delete/$', login_required(views.Clear_Chat), name='messages_delete'),
   
]