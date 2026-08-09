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

