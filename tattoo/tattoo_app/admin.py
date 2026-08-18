from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import User, Client, Appointments

admin.site.register(User, UserAdmin)



class ClientAdmin(admin.ModelAdmin):
    ...

admin.site.register(Client, ClientAdmin)


class AppointmentsAdmin(admin.ModelAdmin):
    ...

admin.site.register(Appointments, AppointmentsAdmin)
