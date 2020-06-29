from .models import Project
from django.conf import settings

class Favorite(object):
    def __init__(self, request):
        """Инициализация объекта корзины."""
        self.session = request.session
        favorite = self.session.get(settings.FAVORITE_SESSION_ID)
        if not favorite:
            # Сохраняем в сессии пустую корзину.
            favorite = self.session[settings.FAVORITE_SESSION_ID] = {}
        self.favorite = favorite

    
    def add(self, project, ids):
        """Добавление товара в корзину или обновление его количества."""
        project_id = str(project.id)
        if project_id not in self.favorite:
            self.favorite[project_id] = {'ids': project_id, 'name': str(project.project_name)}
        self.save()

    def save(self):
        # Помечаем сессию как измененную
        self.session.modified = True

    def remove(self, project):
        """Удаление товара из корзины."""
        project_id = str(project.id)
        if project_id in self.favorite:
            del self.favorite[project_id]
            self.save()
    
    def __iter__(self):
        """Проходим по товарам корзины и получаем соответствующие объекты project."""
        project_ids = self.favorite.keys()
        # Получаем объекты модели Product и передаем их в корзину.
        projects = Project.objects.filter(id__in=project_ids)

        favorite = self.favorite.copy()

        for project in projects:
            favorite[str(project.id)]['project'] = project
        
        for item in favorite.values():
            item['name'] = str(item['name'])
            yield item
    
    # def __len__(self):
    #     """Возвращает общее количество товаров в корзине."""
    #     return sum(int(item['ids']) for item in self.favorite.values())

    def clear(self):
        # Очистка корзины.
        del self.session[settings.FAVORITE_SESSION_ID]
        self.save()