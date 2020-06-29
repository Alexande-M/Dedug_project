from django.urls import path,include
from . import views
from django.conf.urls import url
# from .models import BookmarkProject
from django.contrib.auth.decorators import login_required

urlpatterns = [
    
    url('project-list/', views.ProjectListView.as_view(), name='project_list'),
    url(r'^project-detail/(?P<pk>\w+)/$', views.Project_Detai, name='project_detail'),

    path('account/favorites/', views.Favorite_detail, name='Favorite_detail'),
    path('account/favorites/add/<int:project_id>/', views.Favorite_add, name='Favorite_add'),
    path('account/favorites/remove/<int:project_id>/', views.Favorite_remove, name='Favorite_remove'),
]