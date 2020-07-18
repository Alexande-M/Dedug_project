from django.shortcuts import render, redirect,get_object_or_404
from .models import Category, Project, ProjectaAnalytics,ProjectManager
from django.views import generic
from .forms import  FavoriteAddProjectForm
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Group
from .favorites import Favorite
from django.views.decorators.http import require_POST
from datetime import date
from django.utils import timezone
from Account.models import Subscription
from Account.models import Profile
from django.contrib.auth.models import User
from django.db.models import Q


class Filter_data_Project:
    def get_category(self):
        return Category.objects.all()

    def get_type(self):
        return ProjectManager.CHOICES_PROJECT

class ProjectListView(Filter_data_Project, generic.ListView):
    """Страница со списком проектов"""
    model = Project
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chek_subscribe'] = Subscription.objects.get(user = self.request.user).subscription_end_date
        context['today_date'] = date.today
        self.queryset = Project.objects.filter(project_comletion = False).order_by('-publication_date')
        promotions = self.queryset.filter(promotions = True)
        project_list = []

        # Цикл формирует сортировку списка с проектами 
        for index, project in enumerate(self.queryset):
            for promotion in promotions:
                if index in [5,10,15]: # Периуд индекса через n проходов чтобы чаще встречались продвигаемые проекты  !
                    project_list.append(promotion)
                    if promotion in project_list:
                        break
            project_list.append(project)
            

        print(project_list)

        context['project_list'] = project_list
        return context# Проверка на подписку 
    # elif has_group(request.user, "Seller") or has_group(request.user, "Investor"):
        


def Project_Detai(request, pk):
    """Страница с детальным разбором проекта"""
    projects = Project.objects.filter(pk=pk) 

    """Получение / Создание счётчика посещений на страницу с определённым pk"""
    obj, created = ProjectaAnalytics.objects.get_or_create(
        defaults={
            "project": projects[0],
        }, 
            project = projects[0],
        )
    obj.views += 1  # Увелечение счётчика при каждом посещении 
    obj.save(update_fields=['views']) #Обнавление поля просмотров

    #Объект для обновления поля просмотров у проекта 
    projects_update = Project.objects.get(id = projects[0].id)
    projects_update.count_views_project = obj.views
    projects_update.save(update_fields=['count_views_project'])#Обнавление поля числа просмотров у проекта 

    views = ProjectaAnalytics.objects.filter(project = projects[0]) #Вывод Кол-во просмотров проекта 
    contact_data = Profile.objects.get(user = projects[0].project_author)
    contact_data_email = User.objects.get(id = projects[0].project_author.id).email

    context = {
        'projects': projects,
        'form' : FavoriteAddProjectForm(),
        'views' : views,
        'contact_data': contact_data,
        'contact_data_email':contact_data_email,
    }

    return render(request , 'ProjectManager/project_detail.html', context)


class SearchFilter(generic.ListView):
    def get_queryset(self):
        return Project.objects.filter(project_name__icontains = self.request.GET.get('q'))
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q')
        context['chek_subscribe'] = Subscription.objects.get(user = self.request.user).subscription_end_date
        context['today_date'] = date.today
        return context


class FilterProject(Filter_data_Project, generic.ListView):
    def get_queryset(self):
        
        queryset = Project.objects.filter(
                Q(category__in = self.request.GET.getlist('category')) |  
                Q(choices__in = self.request.GET.getlist('choices')) 
            )
        return queryset

def Favorite_add(request, project_id):
    if  has_group(request.user, "Seller"):
        return redirect('/account/')
    """Функция добавления сессии на избранные проекты"""
    favorite = Favorite(request) # Получение экземпляра сессии 
    project = get_object_or_404(Project, id=project_id) # Получение id проекта 
    favorite.add(project=project,
                        ids=True)
    return redirect('Favorite_detail')


def Favorite_remove(request, project_id):
    """Функция удаление сессии на избранные проекты"""
    if  has_group(request.user, "Seller"):
        return redirect('/account/')
    favorite = Favorite(request)
    project = get_object_or_404(Project, id=project_id)
    favorite.remove(project)
    return redirect('Favorite_detail')


def Favorite_detail(request):
    """Страница со всеми проетами"""
    if  has_group(request.user, "Seller"):
        return redirect('/account/')
    favorite = Favorite(request)
    return render(request, 'Account/favorite_detail.html', {'favorite': favorite})



    


def has_group(user, group_name): 
    try: 
        group = Group.objects.get(name=group_name) 
    except Group.DoesNotExist: 
        return False
    return group in user.groups.all() 