from django.db import models
from django.urls import reverse
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import auth
from django.conf import settings
from django.utils.text import slugify



class Category(models.Model):
    """Категории"""
    # name - Имя категории 
    name = models.CharField("Категория", max_length=150)

    # url - Ссылка на категории 
    url = models.SlugField(max_length=160, unique=True)


    def __str__(self): 
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"



class ProjectManager():
    """Параметры проекта"""
    CHOICES_PROJECT = (
        ('Selling', 'Selling'),
        ('Investing', 'Investing'),
    )       

    

class Project(models.Model):
    """Проект"""

    # Имя проекта 
    project_name = models.CharField("Название проекта", max_length = 100)

    # Связь со всеми категориями на сайте 
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete = models.SET_NULL, null = True)

    # Призентация 
    presentation = models.TextField("Описание проекта")
    
    # Тип проекта 
    choices = models.CharField(max_length = 15, choices = ProjectManager().CHOICES_PROJECT, default='investing')
    
    # Полное описание для проекта 
    full_project_description = models.FileField("Полное описание проекта", upload_to='uploads/%Y/%m/%d/',blank=False)
    
    # Бизнес план 
    business_plan = models.FileField("Бизнес план", upload_to='uploads/%Y/%m/%d/',blank=False)

    # Фото проекта 
    project_img_one = models.ImageField( upload_to='uploads/images/%Y/%m/%d/',blank=True)

    # Фото проекта 
    project_img_two = models.ImageField( upload_to='uploads/images/%Y/%m/%d/',blank=True)

    # Фото проекта 
    project_img_three = models.ImageField( upload_to='uploads/images/%Y/%m/%d/',blank=True)

    
    # Ссылка на проект 
    slug = models.SlugField(max_length=130, unique=False)
    
    # Черновой вариант 
    draft = models.BooleanField("Черновик", default = False)
    
    # Стоимость проекта 
    project_cost = models.PositiveIntegerField("Стоимость проекта",  help_text = "Указывать сумму в рублях")
    
    # Сумма инвестиции 
    project_investment  = models.PositiveIntegerField("Сумма инвестиции",  help_text = "Указывать сумму в рублях", blank=False)
    
    # Универсальность проекта 
    universality = models.BooleanField("Универсальность проека", default = False)
    
    # Статус проверки на корректность 
    status_active_of_project = models.BooleanField("Статус активности проекта", default = False)#
    
    # Дата публикации 
    publication_date = models.DateField("Дата публикации", default=date.today, db_index=True)
    
    # Автор поекта 
    project_author = models.ForeignKey(User, on_delete=models.CASCADE)

    # Продвижение в топ 
    promotions = models.BooleanField("Продвижение проекта", default = False)

    # Статус оплаты  
    payment_state = models.BooleanField("Статус оплаты", default = False)

    #Статус завершения проекта
    project_comletion = models.BooleanField("Статус завершения проекта", default = False)


    # popular = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='Популярность проекта', blank=True)
    
    def __str__(self):
        return self.project_name

    def get_absolute_url(self):
        return reverse('project_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"



class ProjectaAnalytics(models.Model):
    class Meta:
        db_table = "ProjectaAnalytics"

    # внешний ключ на статью
    project = models.ForeignKey(Project, on_delete = models.CASCADE ) 

    # количество просмотров в эту дату
    views = models.IntegerField('Просмотры', default=0) 

    def __str__(self):
        return self.project.project_name

