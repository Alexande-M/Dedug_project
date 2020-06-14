from django.urls import path, include, path
from . import views
from django.conf.urls import url

app_name = 'Payment'
urlpatterns = [
	url(r'^success/$', views.success, name='success'),
	url(r'^fail/$', views.fail, name='fail'),
]