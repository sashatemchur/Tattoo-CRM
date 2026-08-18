from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin



urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-up/code/', views.sign_up_code, name='sign_up_code'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('sign-in/password-recovery/', views.sign_in_password_recovery, name='sign_in_password_recovery'),
    path('logout/', views.logout_user, name='logout_user'),
    path('profile/', views.profile, name='profile'),
    path('profile/add_client/', views.add_client, name='add_client'),
    path('profile/clients/', views.clients, name='clients'),
    path('profile/client/<int:id_client>/delete/', views.delete_client, name='delete_client'),
    path('profile/new-session/', views.new_session, name='new_session'),
    path('profile/clients/search/', views.clients_search, name='clients_search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)