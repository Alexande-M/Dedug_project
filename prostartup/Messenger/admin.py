from django.contrib import admin
from .models import  Chat, Message,SettingsChat
# Register your models here.
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass


@admin.register(SettingsChat)
class SettingsChatAdmin(admin.ModelAdmin):
    pass

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass