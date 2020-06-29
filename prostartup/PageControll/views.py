from django.shortcuts import render



def e_handler404(request, exception):
    """Переопределения страницы 404"""
    return render(request,'404.html', status=404)

def e_handler500(request):
    """Переопределения страницы 500"""
    return render(request, '404.html', status=500) 
    
def page_not_found(request): # delete on production
    return render(request, '404.html')  

def Home(request):
    """Домашняя страница"""
    return render(request, 'Home.html')

def Privacy_policy(request):
    
    """Политика Конфиденциальности"""
    return render(request, 'privacy.html')

def Complete_project(request):
    """Страница с завершёнными проектами"""
    return render(request, 'complete_project.html')