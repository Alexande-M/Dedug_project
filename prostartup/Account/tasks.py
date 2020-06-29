from celery import task
from .models import Subscription
import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

@task
def check_subcription(user):
    user_sub = Subscription.objects.get(user_id = user)
    print("status is " + str(user_sub.status))
    if user_sub.subscription_end_date < datetime.date.today():
        if user_sub.status == True:
            user_sub.status = False
            user_sub.save(update_fields=['status'])
            user_email  = User.objects.get(id = user_sub.user.id)

            subject = ''

            from_email = settings.EMAIL_HOST_USER
            to_email = ['code-gane@mail.ru']
            message = 'Dear {},\n\n\
                    Your Subscription is end'
            mail_sent = send_mail(subject,message,from_email,to_email,fail_silently=False,)
        return mail_sent





