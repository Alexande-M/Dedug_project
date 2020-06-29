from django.urls import path, include, path
from . import views
from django.conf.urls import url
from django.urls import reverse

# app_name = 'Account'
urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('', views.account, name='account'),
    path('subcriptions/', views.Subscription_Investor, name='Subscription_Investor'),
    path('create-project/', views.ProjectCreate.as_view(), name='create_project'),
    url(r'^(?P<pk>\d+)/update/$', views.ProjectUpdate.as_view(), name='project_update'),
    url(r'^(?P<pk>\d+)/delete/$', views.ProjectDelete.as_view(success_url="/account/"), name='project_delete'),
    path('edit-project/', views.EditProject, name='Edit-project'),
    path('register/Seller/', views.Register_Seller, name='Register_Seller'),
    path('register/Investor/', views.Register_Investor, name='Register_Investor'),
    path('register/Buyer/', views.Register_Buyer, name='Register_Buyer'),
    path('', include('Payment.urls')),
    path('edit/', views.Edit, name='Edit'),
    path('history/',views.history, name='history' ),

    path(r'^(?P<id_notifications>\d+)/$', views.read_notifications, name = 'read_notifications')
]

