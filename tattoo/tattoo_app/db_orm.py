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
from tattoo_app.models import User, Client, Appointment
from asgiref.sync import async_to_sync 
from django.utils import timezone
from django.contrib.auth import authenticate

import re
from django.db.models import Q

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




def search_clients_with_surname(search, whose_client):
    if any(char.isdigit() for char in search):
        search = re.sub(r"\D", "", search)
        if search.isdigit():
            clients = Client.objects.filter(telephone__icontains=search, whose_client=whose_client)
            return clients
    else:
        clients = Client.objects.filter(Q(name__icontains=search) | Q(surname__icontains=search), whose_client=whose_client)
        return clients






def add_session_client(id_appointment, date_session_appointment, time_start_appointment, duration_minutes_appointment, price_appointment, service_appointment, notes_appointment):
    client_appointment = Client.objects.get(id=id_appointment)
    appointment = Appointment.objects.create(
        client=client_appointment,
        date_session=date_session_appointment,
        time_start=time_start_appointment,
        duration_minutes=int(duration_minutes_appointment),
        price=price_appointment,
        service=service_appointment,
        notes=notes_appointment,
    )
    return appointment



def session_today(clients):
    dict_session = {
        "all": 0,
        "completed": 0,
        "scheduled": 0
    }
    today = timezone.now().date()
    for client in clients:
        for appointment in client.appointments.all():
            if today == appointment.date_session and appointment.status == "scheduled":
                dict_session["scheduled"] += 1
            elif today == appointment.date_session and appointment.status == "completed":
                dict_session["completed"] += 1


    dict_session["all"] = dict_session["completed"]+dict_session["scheduled"]

    return dict_session

    
def session_today_all_info(user):
    today = timezone.now().date()


    today_appointments = Appointment.objects.filter(
        date_session=today,
        client__whose_client=user
    ).select_related('client')


    return today_appointments



def get_client_for_id(id_client, whose_client):
    try:
        client = Client.objects.get(id=id_client, whose_client=whose_client)
        return client
    except:
        return False


def count_session_client_for_id(id_client, whose_client):
    client = Client.objects.get(id=id_client, whose_client=whose_client)
    return client.appointments


def delete_for_id_appointment(id_appointment):
    appointment = Appointment.objects.get(id=id_appointment)
    appointment.delete()