from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save



from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from datetime import date 
from django.utils import timezone

class Operations(models.Model):
    operation_name = models.CharField("Название операции", max_length=255 ,blank=False)
    operation_summ = models.PositiveIntegerField("Сумма", blank=False)

    def __str__(self):
        return self.operation_name

class Personalaccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key = True)
    summ = models.PositiveIntegerField("Сумма в рублях", default = 599)

    def __str__(self):
        return self.user.username




@receiver(post_save, sender=User)
def save_or_create_personalaccount(sender, instance, created, **kwargs):
    if created:
        Personalaccount.objects.create(user=instance)
    else:
        try:
            instance.personalaccount.save()
        except ObjectDoesNotExist:
            Personalaccount.objects.create(user=instance)



from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
