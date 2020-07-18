from django.contrib import admin
from .models import Profile,Subscription, Notifications


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo','role']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription_date', 'subscription_end_date', 'status']


@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'text','pub_date']


