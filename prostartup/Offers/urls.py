from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth.decorators import login_required


app_name = 'Offers'

urlpatterns = [
    url(r'^account/offers/$', login_required(views.OffersAllView.as_view()), name='offers'),
    url(r'^account/offers/create/(?P<project_id>\d+)/(?P<user_id>\d+)/$', login_required(views.CreateOffersView.as_view()), name='create_offer'),
    url(r'^account/offers/remove/(?P<offer_id>\d+)/$', login_required(views.OffersRemoveView.as_view()), name='remove_offer'),
    
    url(r'^account/contract/$', login_required(views.ContractView.as_view()), name = 'contract'),
    url(r'^account/contract/(?P<contract_id>\d+)$', login_required(views.ContractDatailView.as_view()), name = 'contract_detail'),
    url(r'^account/contract/create/(?P<offer_id>\d+)$', login_required(views.ContractCreateView.as_view()), name = 'contract_create'),
    # url(r'^$', login_required(views.ContractView.as_view()), name = 'contract'),
   
]