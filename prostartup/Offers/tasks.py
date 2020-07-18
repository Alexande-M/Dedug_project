from celery import task
from django.core.mail import send_mail
from .models import Contract
from django.conf import settings
from django.contrib.auth.models import User


@task
def contract_created(contract_id):
    """Задача отправки email-уведомлений при успешном оформлении заказа."""

    contract = Contract.objects.get(id=contract_id)
    from_user_email  = User.objects.get(id = contract.from_user.id)
    to_user_email = User.objects.get(id = contract.to_user.id)

    subject = 'Order nr. {}'.format(contract.id)

    from_email = settings.EMAIL_HOST_USER
    to_email = [to_user_email.email, from_user_email.email]
    message = 'Dear {},\n\nYou have successfully placed an order.\
               Your order id is {}.'.format(contract.from_user.first_name, contract.id)

    mail_sent = send_mail(subject,message,from_email,to_email,fail_silently=False,)
    return mail_sent