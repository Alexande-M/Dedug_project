from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404,redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, SubscriptionFormData, RefaillForm,CreateProjectForm
from django.contrib.auth.models import Group
from .models import Profile, Subscription
from django.contrib import messages
from django.views import generic
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from ProjectManager.models import Project
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
import datetime
from django.contrib.auth.decorators import login_required
from django.views import View
from Offers.models import Offer




def logout_view(request):
    logout(request)
    return redirect('/')

def Set_Subscription(request, template, tag):
    
    sub_data = Subscription.objects.get(user=request.user)

    if request.method == 'POST':
        sub_form = SubscriptionFormData(request.POST)
        if sub_form.is_valid():
            month = sub_form.cleaned_data.get("cost") # @@@@@@@@@@@@@@@
            new_Sub = sub_form.save(commit=False)


            # new_Sub.user = User.objects.get(id = request.user.id)
            new_Sub.user = request.user
            
            if month == "1":# @@@@@@@@@@@@@@@
                new_Sub.subscription_end_date = datetime.date.today() + datetime.timedelta(1*365/12)# @@@@@@@@@@@@@@@
            elif month == "2":# @@@@@@@@@@@@@@@
                new_Sub.subscription_end_date = datetime.date.today() + datetime.timedelta(2*365/12)# @@@@@@@@@@@@@@@
            elif month == "3":# @@@@@@@@@@@@@@@
                new_Sub.subscription_end_date = datetime.date.today() + datetime.timedelta(3*365/12)# @@@@@@@@@@@@@@@
            
            
            new_Sub.save()
            sub_data.status = True
            sub_data.save(update_fields=['status'])

            return redirect('/account/')
    else:
        sub_form = SubscriptionFormData()

    
    context = {
        'sub_form' : sub_form,
        'sub_data': sub_data,
    }
    return render(request,template, context )



@login_required(login_url='/account/login/')
def Subscription_Investor(request):
    if not (has_group(request.user, "Investor") or has_group(request.user, "Buyer")):
        return redirect('/account/')

    tag = 'costBuy'
    tamplate = 'registration/Subscription_Investor.html'
    return Set_Subscription(request, tamplate,tag)


def Register(request, role, tamplate):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password_one'])
            new_user.save()
            group = Group.objects.get(name=role)
            new_user.groups.add(group)
            new_user.save()
            return redirect('/account/')

    else:
        user_form = UserRegistrationForm()
    return render(request,tamplate,{'user_form': user_form,'role': role})


def Register_Seller(request):
    role = 'Seller'
    tamplate = 'registration/Register_Seller.html'
    return Register(request, role, tamplate)

def Register_Investor(request):
    role = 'Investor'
    tamplate = 'registration/Register_Investor.html'
    return Register(request, role, tamplate)


def Register_Buyer(request):
    role = 'Buyer'
    tamplate = 'registration/Register_Buyer.html'
    return Register(request, role, tamplate)





class ProjectCreate(LoginRequiredMixin, CreateView):# Вход в админпанель 
    form_class = CreateProjectForm
    model = Project
    success_url = '/account/'
    
    def form_valid(self, form):
        form.instance.project_author = self.request.user
        form.instance.slug = form.instance.project_name
        return super().form_valid(form)


class ProjectUpdate(LoginRequiredMixin,UpdateView):# Вход в админпанель 
    model = Project
    # fields = '__all__' 'category',
    fields = ('project_name', 'presentation','full_project_description', 'business_plan', 'project_cost', 'project_investment','status_active_of_project')
    template_name_suffix =  '_update_form'
    

class ProjectDelete(LoginRequiredMixin,DeleteView):# Вход в админпанель 
    model = Project
    fields = '__all__'













from django.contrib.auth.hashers import check_password # Доделать смену пароля !!!!!!!!!!!!!!!!!!!!!!!!!!!!
@login_required(login_url='/account/login/')
def Edit(request):  # Вход в админпанель 
    data_profile = Profile.objects.get(user = request.user)
    profile = load_profile(request.user)
    u = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=profile,data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():

            old_pass = request.POST.get("old_pass")
            new_pass = request.POST.get("new_pass")
            new_pass_rep = request.POST.get("new_pass_rep")


            new_password = user_form.cleaned_data['new_pass']
            new_passwordrep = user_form.cleaned_data['new_pass_rep']


           

            # print(check_password(old_pass, u.password))

            if check_password(old_pass, u.password):

                # print(str(new_password == new_pass_rep) +'  '+str(new_password) +'  '+ str(new_pass_rep))

                if new_password == new_pass_rep:

                    shange_pass = user_form.save(commit=False)
                    shange_pass.set_password(new_password)
                    shange_pass.save()
                    messages.success(request, 'Password updated successfully')
                else:
                    messages.error(request, 'password don t equal')
                
            else:
                messages.error(request, 'Profile don t updated successfully')

            user_form.save()
            profile_form.save()
            
            messages.success(request, 'Profile updated successfully')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile)
    return render(
        request,
        'Account/edit_profile.html',
        {'user_form': user_form, 'profile_form': profile_form , 'data_profile' : data_profile}
    )




@login_required(login_url='/account/login/')
def EditProject(request):# Вход в админпанель 
    all_project = Project.objects.filter(project_author=request.user, project_comletion = False)
    context = {
        'projects': all_project
    }
    return render(request, 'Account/edit_project.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth, messages
from django.dispatch import receiver
from django.http import HttpResponse
from hashlib import sha256
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .tasks import check_subcription

from django.contrib.auth.models import User

@login_required(login_url='/account/login/')
def account(request):# Вход в админпанель 
    data_profile = Profile.objects.get(user = request.user) 

    



    if request.method == 'POST':

        form_ref = RefaillForm(request.POST)
        if form_ref.is_valid():
            out_summ = form_ref.cleaned_data['summ']

            mrh_login = "Prostart-Up"
            mrh_pass1 = "w3e8KYf2k48tbfgVXkvI"
            inv_id  = "1"
            inv_desc  = "Пополнение баланса"
            
            #Формирование контрольной суммы
            result_string = "{}:{}:{}:{}".format(mrh_login, out_summ, inv_id, mrh_pass1)
            sign_hash = sha256(result_string.encode())
            crc = sign_hash.hexdigest().upper()
            url = "https://auth.robokassa.ru/Merchant/Index.aspx?MrchLogin={}&OutSum={}&InvId={}&Desc={}&SignatureValue={}".format(mrh_login, out_summ, inv_id, inv_desc, crc)
            if request.method == "POST":
                #К примеру запись в талицу пополнения

                #Переход на страницу оплаты в робокасса
                return redirect(url)
    else:
         form_ref = RefaillForm()

    id = request.user.id
    if has_group(request.user, "Seller"):
        template = 'Account/my_project.html'
        all_project = Project.objects.filter(project_author=request.user)
        offers = Offer.objects.filter(to_user__in=[request.user.id], deal = False)
        context = {
            'projects': all_project,
            'offers': offers
        }
    elif has_group(request.user, "Buyer") or has_group(request.user, "Investor"):

        
        user_id = Subscription.objects.get(user = request.user)
        # Запуск асинхронной задачи.
        # check_subcription.delay(user_id.user.id)

        chek_subscribe = Subscription.objects.get(user = request.user).subscription_end_date
        template = 'Account/investor_and_buyer_admin.html'
        context = {
                'id' : id,
                'chek_subscribe': chek_subscribe,
            } 
    

    context1 = {'form_ref':form_ref, 'data_profile':data_profile}
    context.update(context1)
 
    return render(request,template,context)




def load_profile(user):
  try:
    return user.profile
  except:  # this is not great, but trying to keep it simple
    profile = Profile.objects.create(user=user)
    return profile





# def Chek_auth




def has_group(user, group_name): 
    try: 
        group = Group.objects.get(name=group_name) 
    except Group.DoesNotExist: 
        return False
    return group in user.groups.all() 




