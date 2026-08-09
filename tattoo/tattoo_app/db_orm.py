import os
import sys
import django
import random
from django.db import IntegrityError
# Додаємо корінь проєкту (де лежить manage.py) у sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Вказуємо settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tattoo.settings")
import re
# Запускаємо Django
django.setup()
from asgiref.sync import sync_to_async
from tattoo_app.models import User, Client
from asgiref.sync import async_to_sync 

from django.contrib.auth import authenticate

#@sync_to_async
#def create_user_base_places_exhibitions(chat_id_message, list_info):
#    users = BasePlacesUserExhibitions(chat_id=chat_id_message, base_places_terroir_and_traditions=list_info[0], base_places_collection_co_selection=list_info[1], base_places_snucie=list_info[2],
#                            base_places_art_that_saves_lives=list_info[3], base_places_gotong_royong=list_info[4], base_places_anna_konik=list_info[5],
#                            base_places_uncensored=list_info[6], base_places_jacek_adamas=list_info[7])
#    users.save()


#from django.contrib.auth import authenticate

#user = authenticate(
 #   request,
#    username=email,   # сюди передаєш email
#    password=password
#)

def check_repeat_email(email):
    if User.objects.filter(email=email).exists():
        return False
    return True




def create_user(name, email, password):
    user = User.objects.create_user(
        username=email,
        first_name=name,
        email=email,
        password=password
    )
    return user


def login_user(request, email, password):
    
    user = authenticate(
        request,
        username=email,   
        password=password
    )
    if user is not None:
        return user
    else:
        return False

    
def change_password(email, new_password):
    user = User.objects.get(email=email)
    user.set_password(new_password)
    user.save()




def create_client(name, surname, telephone, date_birth, telegram, email, client_source, allegria, whose_client):
    client = Client.objects.create(
        name=name,
        surname=surname,
        telephone=telephone,
        date_birth=date_birth or None,
        telegram=telegram,
        email=email,
        client_source=client_source,
        allegria=allegria,
        whose_client=whose_client
    )
    return client


def client_delete(id, whose_client):
    client = Client.objects.get(id=id, whose_client=whose_client)
    client.delete()


def search_clients(search, whose_client):
    if any(char.isdigit() for char in search):
        search = re.sub(r"\D", "", search)
        if search.isdigit():
            clients = Client.objects.filter(telephone__icontains=search, whose_client=whose_client)
            return clients
    else:
        clients = Client.objects.filter(name__icontains=search, whose_client=whose_client)
        return clients


