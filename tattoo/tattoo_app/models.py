from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)



class Client(models.Model):
    name = models.CharField('Name', max_length = 500)
    surname = models.CharField('Surname', max_length = 500, blank=True)
    telephone = models.CharField('Telephone', max_length = 500)
    telegram = models.CharField('Telegram', max_length = 500, blank=True)
    email = models.EmailField("Email", blank=True)
    date_birth = models.DateField("Date of birth", blank=True, null=True)
    allegria = models.BooleanField("Allegria", default=False)
    client_source = models.CharField('Client Source', max_length = 500, blank=True)
    created_at = models.DateTimeField("Date created", auto_now_add=True)
    whose_client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clients")

    
    def __str__(self):
        return self.name

    
    class Meta:
        verbose_name = "client"
        verbose_name_plural = "clients"

        constraints = [
            models.UniqueConstraint(
                fields=["whose_client", "telephone"],
                name="unique_client_phone_per_user"
            )
        ]



class Appointments(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="appointments")
    date_session = models.DateField("Date of session")
    time_start = models.TimeField("Time start")  
    duration_minutes = models.IntegerField("Duration minutes") 
    price = models.DecimalField("Price", max_digits=8, decimal_places=2) 
    service = models.CharField('Service', max_length = 500)
    notes = models.CharField('Notes', max_length = 500, blank=True)


    def __str__(self):
        return self.client.name

    
    class Meta:
        verbose_name = "appointment"
        verbose_name_plural = "appointments"

