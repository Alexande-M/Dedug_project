from django.shortcuts import render
from .models import Chat, SettingsChat,Message
from Account.models import Profile
from django.shortcuts import render, redirect
from .forms import MessageForm
from django.db.models import Count
from django.urls import reverse
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.http import HttpResponse
from django.core import serializers


def filter(request,chat_id):
    chat = Message.objects.filter(chat_id=chat_id)
    mess_list = []
    for i in chat:
        mess_list.append({'author' : str(i.author), 'message' : str(i.message),'is_readed': str(i.is_readed) })
    # results_json = serializers.serialize('json', chat)
    return HttpResponse(json.dumps(mess_list,   ensure_ascii=False), content_type='application/json')


  










class DialogsView(View):
    def get(self, request):
        chats = Chat.objects.all().filter(members__in=[request.user.id])
        settings = SettingsChat.objects.filter(user = request.user)

        count_is_readed = Message.objects.values_list('message',flat=True).filter(author = request.user, is_readed = False).count()

        return render(request, 'users/dialogs.html',{'user_profile': request.user,'chats': chats,'settings':settings,'count_is_readed':count_is_readed})


class MessagesView(View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
                ID_PAGE = chat_id
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None
        return render(
            request,
            'users/messeg.html',
            {
                'user_profile': request.user,
                'chat': chat,
                'form': MessageForm(),
                'ID_PAGE':ID_PAGE ,
            }
        )
 
    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('Messenger:messages', kwargs={'chat_id': chat_id}))



class CreateDialogView(View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        try:
            if chats.count() == 0:
                chat = Chat.objects.create()
                chat.members.add(request.user)
                chat.members.add(user_id)
                chat_two = Chat.objects.get(members__in=[user_id])
                # chat_one = Chat.objects.get(members__in=[request.user.id])
                settings_for_one_person = SettingsChat.objects.create(chat = chat_two, user = request.user )
                settings_for_two_person = SettingsChat.objects.create(chat = chat_two, user_id = user_id)
            else:
                chat = chats.first()
        except:
            pass
        return redirect(reverse('Messenger:messages', kwargs={'chat_id': chat.id}))






class Clear_ChatView(View):
    def get(self, request, chat_id):
        try:
            chats = Chat.objects.get(id = chat_id)
            if chats:
                chat = SettingsChat.objects.filter(chat=chats, user = request.user)
                # chat.visibility = False
                chat.update(visibility = False)
        except:
            pass
        return redirect(reverse('dialogs'))
