from django.shortcuts import render
from .models import Offer, Contract
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.db.models import Count
from django.urls import reverse
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from ProjectManager.models import Project
from Account.models import Notifications
from django.contrib.auth.models import User

from .tasks import contract_created


class ContractCreateView(View):
    def get(self, request, offer_id):
        contracts_offer = Offer.objects.get(id=offer_id)
        close_project = Project.objects.get(id = contracts_offer.member.id)
        users_list = [contracts_offer.to_user,contracts_offer.from_user]
        if contracts_offer:
            contract = Contract.objects.create(
                offer_id = contracts_offer,
                from_user = contracts_offer.to_user,
                to_user = contracts_offer.from_user,
                project_id = contracts_offer.member
            )

            for user in users_list:
                notifications = Notifications.objects.create(
                    user = user,
                    title = 'Контракт заключён ! Поздравляем вас.',
                    text = """Контракт ID:%s заключён.<br> Можете с ним \
                                    <a href='/account/contract/%s/'>ознакомится !</a>""" %  (contract.id,contract.id)
                )

            close_project.project_comletion = True
            close_project.save(update_fields=['project_comletion'])
            contracts_offer.deal = True
            contracts_offer.save(update_fields=['deal'])
            contract.save()

            # Запуск асинхронной задачи.
            # contract_created.delay(contract.id)
        else:
            contract = contracts_offer.first()
        
        return redirect(reverse('Offers:contract'))



class ContractDatailView(View):
    # Output Datale Contract
    def get(self, request, contract_id):
        contracts = Contract.objects.filter(id=contract_id)
        if contracts.count() == 0:
            return redirect('/account/')

        project_id = contracts[0].project_id.id # ДОП ДАННЫЕ
        project = Project.objects.get(id = project_id).project_name # ДОП ДАННЫЕ
        return render(
            request,
            'Account/contract_details.html',
            {
                'contracts' : contracts,
                'project'  : project, # ДОП ДАННЫЕ
            }
        )

class ContractView(View):
    def get(self, request):
        template = 'Account/contract.html'
        if  has_group(request.user, "Seller"):
            contracts = Contract.objects.filter(from_user__in=[request.user.id])
        elif has_group(request.user, "Investor") or has_group(request.user, "Buyer"):
            contracts = Contract.objects.filter(to_user__in=[request.user.id])
                
        return render(request, template,{'user_profile': request.user,'contracts': contracts,})



class OffersAllView(View):
    def get(self, request):
        if  has_group(request.user, "Seller"):
            return redirect('/account/')
        elif has_group(request.user, "Investor") or has_group(request.user, "Buyer"):
            return redirect('/account/')
            
            # template = 'Account/investor_and_buyer_admin.html'
        return render(request, template,{'user_profile': request.user,})


class OffersRemoveView(View):
    def get(self, request, offer_id):
        user = Offer.objects.get(id=offer_id)
        # offers = Offer.objects.filter(id=offer_id, from_user = request.user,to_user = to_user.to_user)
        if (user.to_user == request.user) or (user.from_user == request.user):
            offer = Offer.objects.get(id=offer_id)
            offer.delete()
            notifications_from = Notifications.objects.create(
                    user = request.user,
                    title = 'Запрос отменён !',
                    text = """Оффер ID:%s удалён !""" %  (offer_id)
                )
        return redirect(reverse('Offers:offers'))


class CreateOffersView(View):
    def get(self, request, project_id, user_id):
        offers = Offer.objects.filter(from_user__id=request.user.id,to_user__id=user_id, member__id=project_id)
        user_to = User.objects.get(id = user_id)
        if offers.count() == 0:
            offer = Offer.objects.create(from_user_id = request.user.id, to_user_id = user_id, member_id = project_id)
            notifications_from = Notifications.objects.create(
                    user = request.user,
                    title = 'Запрос обработан !',
                    text = """Оффер ID:%s запрошен.<br> Пожалуйста ожидайте ответа !""" %  (offer.id)
                )
            notifications_to = Notifications.objects.create(
                    user = user_to,
                    title = 'У вас новый оффер !',
                    text = """Запрошен оффер ID:%s  на ваш <a href='/project-detail/%s/'> проект </a>!""" %  (offer.id,project_id)
                )


        else:   
            offer = offers.first()
        return redirect(reverse('Offers:offers'))


def has_group(user, group_name): 
    try: 
        group = Group.objects.get(name=group_name) 
    except Group.DoesNotExist: 
        return False
    return group in user.groups.all() 


