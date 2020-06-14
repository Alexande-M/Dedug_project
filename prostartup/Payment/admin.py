from django.contrib import admin

from .models import Personalaccount, Operations


@admin.register(Personalaccount)
class Personal_accountAdmin(admin.ModelAdmin):
    pass