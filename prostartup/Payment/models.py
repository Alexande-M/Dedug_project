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
    summ = models.PositiveIntegerField("Сумма в рублях", default = 0)






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

#Модель пополнения	
class Popoln(models.Model):
	class Meta():
		db_table = 'popoln'
		verbose_name = "Пополнение"
		verbose_name_plural = "Пополнения"
		
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	summ = models.FloatField("Сумма", default = 50.00)
	date = models.DateTimeField("Дата покупки", default=timezone.now)
	odobren = models.BooleanField("Успех пополнения", default=False)
	
	def __str__(self):
		return self.user.username

# class Personalaccount(models.Model):
#     class Meta:
#         verbose_name = 'Account'
#         verbose_name_plural = 'Accounts'

#     MAX_TOTAL_BALANCES = 10000000
#     MAX_BALANCE = 10000
#     MIN_BALANCE = 0
#     MAX_DEPOSIT = 1000
#     MIN_DEPOSIT = 1
#     MAX_WITHDRAW = 1000
#     MIN_WITHDRAW = 1
#     id = models.AutoField(
#         primary_key=True,
#     )
#     uid = models.UUIDField(
#         unique=True,
#         editable=False,
#         default=uuid.uuid4,
#         verbose_name='Public identifier',
#     )
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.PROTECT,
#     )
#     created = models.DateTimeField(
#         blank=True,
#     )
#     modified = models.DateTimeField(
#         blank=True,
#     )
#     balance = models.PositiveIntegerField(
#         verbose_name='Current balance',
#     )

#     def deposit(self, amount, deposited_by, asof):
#         assert amount > 0
#         if not self.MIN_DEPOSIT <= amount <= self.MAX_DEPOSIT:
#             raise InvalidAmount(amount)
#         if self.balance + amount > self.MAX_BALANCE:
#             raise ExceedsLimit()
#         total = Account.objects.aggregate(
#             total=Sum('balance')
#         )['total']
#         if total + amount > self.MAX_TOTAL_BALANCES:
#             raise ExceedsLimit()

#         action = self.actions.create(
#             user=deposited_by,
#             type=Action.ACTION_TYPE_DEPOSITED,
#             delta=amount,
#             asof=asof,
#         )
#         self.balance += amount
#         self.modified = asof
#         self.save()

# class Action(models.Model):
#     class Meta:
#         verbose_name = 'Account Action'
#         verbose_name_plural = 'Account Actions'
#     ACTION_TYPE_CREATED = 'CREATED'
#     ACTION_TYPE_DEPOSITED = 'DEPOSITED'
#     ACTION_TYPE_WITHDRAWN = 'WITHDRAWN'
#     ACTION_TYPE_CHOICES = (
#         (ACTION_TYPE_CREATED, 'Created'),
#         (ACTION_TYPE_DEPOSITED, 'Deposited'),
#         (ACTION_TYPE_WITHDRAWN, 'Withdrawn'),
#     )
#     REFERENCE_TYPE_BANK_TRANSFER = 'BANK_TRANSFER'
#     REFERENCE_TYPE_CHECK = 'CHECK'
#     REFERENCE_TYPE_CASH = 'CASH'
#     REFERENCE_TYPE_NONE = 'NONE'
#     REFERENCE_TYPE_CHOICES = (
#         (REFERENCE_TYPE_BANK_TRANSFER, 'Bank Transfer'),
#         (REFERENCE_TYPE_CHECK, 'Check'),
#         (REFERENCE_TYPE_CASH, 'Cash'),
#         (REFERENCE_TYPE_NONE, 'None'),
#     )
#     id = models.AutoField(
#         primary_key=True,
#     )
#     user_friendly_id = models.CharField(
#         unique=True,
#         editable=False,
#         max_length=30,
#     )
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.PROTECT,
#         help_text='User who performed the action.',
#     )
#     created = models.DateTimeField(
#         blank=True,
#     )
#     account = models.ForeignKey(
#         Account,
#     )
#     type = models.CharField(
#         max_length=30,
#         choices=ACTION_TYPE_CHOICES,
#     )
#     delta = models.IntegerField(
#         help_text='Balance delta.',
#     )
#     reference = models.TextField(
#         blank=True,
#     )
#     reference_type = models.CharField(
#         max_length=30,
#         choices=REFERENCE_TYPE_CHOICES,
#         default=REFERENCE_TYPE_NONE,
#     )
#     comment = models.TextField(
#         blank=True,
#     )
#     # Fields used solely for debugging purposes.
#     debug_balance = models.IntegerField(
#         help_text='Balance after the action.',
#     )


#     @classmethod
#     def create(
#         cls,
#         user,
#         account,
#         type,
#         delta,
#         asof,
#         reference=None,
#         reference_type=None,
#         comment=None,
#     ):
#         """Create Action.
#         user (User):
#             User who executed the action.
#         account (Account):
#             Account the action executed on.
#         type (str, one of Action.ACTION_TYPE_\*):
#             Type of action.
#         delta (int):
#             Change in balance.
#         asof (datetime.datetime):
#             When was the action executed.
#         reference (str or None):
#             Reference number when appropriate.
#         reference_type(str or None):
#             Type of reference.
#             Defaults to "NONE".
#         comment (str or None):
#             Optional comment on the action.
#         Raises:
#             ValidationError
#         Returns (Action)
#         """
#         assert asof is not None
#         if (type == cls.ACTION_TYPE_DEPOSITED and
#             reference_type is None):
#             raise errors.ValidationError({
#                 'reference_type': 'required for deposit.',
#             })
#         if reference_type is None:
#             reference_type = cls.REFERENCE_TYPE_NONE
#         # Don't store null in text field.
#         if reference is None:
#             reference = ''
#         if comment is None:
#             comment = ''
#         user_friendly_id = generate_user_friendly_id()
#         return cls.objects.create(
#             user_friendly_id=user_friendly_id,
#             created=asof,
#             user=user,
#             account=account,
#             type=type,
#             delta=delta,
#             reference=reference,
#             reference_type=reference_type,
#             comment=comment,
#             debug_balance=account.balance,
#         )


