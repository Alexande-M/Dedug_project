from django.shortcuts import render, redirect,get_object_or_404
from .models import Category, Project, ProjectaAnalytics
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

class ProjectListView(generic.ListView):
    """Страница со списком проектов"""
    model = Project
    queryset = Project.objects.filter(project_comletion = False) 

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['chek_subscribe'] = Subscription.objects.get(user = self.request.user).subscription_end_date
        context['today_date'] = date.today
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

    views = ProjectaAnalytics.objects.filter(project = projects[0]) #Вывод Кол-во просмотров проекта 

    context = {
        'projects': projects,
        'form' : FavoriteAddProjectForm(),
        'views' : views,
    }
    return render(request , 'ProjectManager/project_detail.html', context)






@require_POST
def Favorite_add(request, project_id):
    if  has_group(request.user, "Seller"):
        return redirect('/account/')
    """Функция добавления сессии на избранные проекты"""
    favorite = Favorite(request) # Получение экземпляра сессии 
    project = get_object_or_404(Project, id=project_id) # Получение id проекта  
    form = FavoriteAddProjectForm(request.POST) # Обработка формы 
    if form.is_valid():
        cd = form.cleaned_data
        # Добавление проекта в избранные 
        favorite.add(project=project,
                        ids=cd['update'])
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