from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from ProjectManager.models import Project
from django.conf import settings
 
class Offer(models.Model):
    member = models.ForeignKey(Project, verbose_name=_("Project"),on_delete=models.CASCADE, default="")
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,related_name='from_users', on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,related_name='to_users', on_delete=models.CASCADE
    ) 

    deal = models.BooleanField(default=False)
    rejected = models.DateTimeField(blank=False, null=True,default=timezone.now)

    def get_absolute_url(self):
        return reverse('Offer:offer', args=[self.pk])

    def __str__(self):
        return "%s awaiting acceptance %s <br> Project: <a href='/project-detail/%s/' style='color:#00b2e7;'>%s</a>" % (self.from_user.username, self.to_user.username, self.member.id,self.member)


class Contract(models.Model):
    offer_id = models.ForeignKey(Offer, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,related_name='from_user', on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,related_name='to_user', on_delete=models.CASCADE
    ) 

    rejected = models.DateTimeField(blank=False, null=True,default=timezone.now)

    def get_absolute_url(self):
        return reverse('Contract:contract', args=[self.pk])


    def __str__(self):
        return 'Contract concluded name of : ' + self.project_id.project_name
