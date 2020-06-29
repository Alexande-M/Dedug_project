from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from datetime import timedelta
from datetime import date 
from django.utils import timezone


class Subscription(models.Model):
    CHOICES_MOUNTH = (
        ('1', '1 month'),
        ('2', '2 month'),
        ('3', '3 month'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key = True)
    subscription_date = models.DateField("Дата оформления подписки", default=date.today, db_index=True)
    cost = models.CharField(max_length=12, choices=CHOICES_MOUNTH , default="1 month")
    subscription_end_date = models.DateField("Конец подписки", default=date.today, db_index=True)
    status = models.BooleanField("Стату подписки : ", default = False)

    def __str__(self):
        return self.cost


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True) #, default='default.png'
    role = models.CharField('Роль: ', max_length=8, blank=True) # Добавить при расширения аккаунта 
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    

class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Заголовок уведомления: ', max_length = 255, blank=True) 
    text = models.TextField('Уведомление:')
    pub_date = models.DateTimeField('Время уведомления', default=timezone.now)
    is_readed = models.BooleanField('Прочитано', default=False)
    

    def __str__(self):
        return self.title
    
@receiver(post_save, sender=User)
def save_or_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_or_create_subscription(sender, instance, created, **kwargs):
    if created:
        Subscription.objects.create(user=instance)
    else:
        try:
            instance.subscription.save()
        except ObjectDoesNotExist:
            Subscription.objects.create(user=instance)






