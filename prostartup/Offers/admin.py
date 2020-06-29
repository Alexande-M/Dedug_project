from django.contrib import admin
from .models import Offer, Contract

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    pass

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    # fields = ['get_member',]
    # list_display = ('get_member',)

    def get_member(self, row):
        return ','.join([x.project_name for x in row.member.all()])


