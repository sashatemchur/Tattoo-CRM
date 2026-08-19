from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import User, Client, Appointment

admin.site.register(User, UserAdmin)



class ClientAdmin(admin.ModelAdmin):
    ...

admin.site.register(Client, ClientAdmin)


class AppointmentAdmin(admin.ModelAdmin):
    ...

admin.site.register(Appointment, AppointmentAdmin)
