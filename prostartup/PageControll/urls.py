from django.urls import path, include, path
from . import views
from django.conf.urls import url
from django.urls import reverse


urlpatterns = [
    path('', views.Home, name='Home'),
    path('privacy-policy/', views.Privacy_policy, name='privacy_policy'),
    path('complete-project/', views.Complete_project, name='complete_project'),
    path('404/', views.page_not_found, name='404'),
]

