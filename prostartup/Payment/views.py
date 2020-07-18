from django.shortcuts import render
from .models import Personalaccount
#from .forms import PersonalaccountForm, RefaillForm
from django.contrib.auth.models import User
from django.shortcuts import render,redirect,get_object_or_404,redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth, messages
from .forms import  PersonalaccountForm
from django.dispatch import receiver
from django.http import HttpResponse
from hashlib import sha256
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


#Проверка плотежа
@csrf_exempt
def res(request):
	if not request.method == 'POST':
		return HttpResponse('error')
	mrh_pass2 = "NwSGyBY57xPBYL4Uy8c9"
    #Проверка заголовка авторизации
	if request.method == 'POST':
		out_summ = request.POST['OutSum']
		inv_id = request.POST['InvId']
		crc = request.POST['SignatureValue']
		crc = crc.upper()
		crc = str(crc)
		#Формирование своей контрольной суммы
		result_string = "{}:{}:{}".format(out_summ, inv_id, mrh_pass2)
		sign_hash = sha256(result_string.encode())
		my_crc = sign_hash.hexdigest().upper()
		#Проверка сумм
		if my_crc not in crc:
			# Ответ ошибки
			context = "bad sign"
			return HttpResponse(context)
		else:
			#Ответ все верно
			context = "OK{}".format(inv_id)
			return HttpResponse(context)

#Платеж принят
@csrf_exempt
def success(request):
	if not request.method == 'POST':
		return HttpResponse('error')
	
	payment = Personalaccount.objects.get(user = request.user)
	mrh_pass1 = "w3e8KYf2k48tbfgVXkvI"
    #Проверка заголовка авторизации
	if request.method == 'POST':
		out_summ = request.POST['OutSum']
		inv_id = request.POST['InvId']
		crc = request.POST['SignatureValue']
		crc = crc.upper()
		crc = str(crc)
		#Формирование своей контрольной суммы
		result_string = "{}:{}:{}".format(out_summ, inv_id, mrh_pass1)
		sign_hash = sha256(result_string.encode())
		my_crc = sign_hash.hexdigest().upper()
		#Проверка сумм
		if my_crc not in crc:
			#Ошибка
			context = "bad sign"
			return HttpResponse(context)
		else:
			#Показ страницы успешной оплаты
			sum = payment.summ
			payment.summ = sum + out_summ
			payment.save(update_fields=['summ'])

			return render(request, 'Payment/success.html')

#Платеж не принят
@csrf_exempt
def fail(request):
	if request.method == "POST":
		return render(request, 'Payment/fail.html')
