from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, handler404, handler500 
from Account.views import logout_view

handler404 = 'PageControll.views.e_handler404'
handler500 = 'PageControll.views.e_handler500'

urlpatterns = [
    path('admin/logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
   
]

#My urls
urlpatterns += [
    path('',         include('ProjectManager.urls')),
    path('account/', include('Account.urls')),
     
    path('account/messege/', include(('Messenger.urls', 'Messenger'), namespace='Messenger')),
    path('account/payment/', include('Payment.urls')),
    path('',  include(('Offers.urls', 'Offers'), namespace='Offers')),
    path('',  include('PageControll.urls')),

] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  


