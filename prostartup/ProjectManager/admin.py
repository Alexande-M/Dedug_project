from django.contrib import admin
from .models import Category, Project, ProjectaAnalytics

@admin.register(ProjectaAnalytics)
class ProjectaAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'views') # отображаемые поля в админке
    search_fields = ('__str__', ) # поле, по которому производится поиск


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('name',)}



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'category', 'choices', 'universality', 'status_active_of_project', 'publication_date', 'project_author')
    prepopulated_fields = {'slug': ('project_name',)}
