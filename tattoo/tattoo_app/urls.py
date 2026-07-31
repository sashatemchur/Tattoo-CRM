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
    path('profile/', views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)