from django.urls import path,include
from . import views
from django.conf.urls import url
# from .models import BookmarkProject
from django.contrib.auth.decorators import login_required

urlpatterns = [
    
    url('project_list/', views.ProjectListView.as_view(), name='project_list'),
    url(r'^project_all/(?P<pk>\w+)/$', views.Project_Detai, name='project_detail'),


    path('account/favorites/', views.Favorite_detail, name='Favorite_detail'),
    path('account/favorites/add/<int:project_id>/', views.Favorite_add, name='Favorite_add'),
    path('account/favorites/remove/<int:project_id>/', views.Favorite_remove, name='Favorite_remove'),

    path('404/', views.page_not_found, name='404'), # delete on productions
    path('', views.Home, name='Home'),
]