from django.shortcuts import render,redirect
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings


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

def About_us(request):
    """Страница О нас"""
    return render(request, 'about-us.html')

def Contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            name = form.cleaned_data.get("name")
            subject = form.cleaned_data.get("subject")
            massage = form.cleaned_data.get("massage")
            to_email = settings.EMAIL_HOST_USER
            send_mail(subject,
                      massage + '\nОт пользователя: '+ email,
                      to_email,
                      [to_email],
                      fail_silently=False,
                    )
            return redirect('/contact-us/')
        else:
            pass 
    else:
        form = ContactForm()    
    context = {
        'form' : form,
    }
    return render(request, 'contact-us.html',context)