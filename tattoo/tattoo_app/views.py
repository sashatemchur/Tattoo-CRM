from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import httpx, asyncio
import json
import requests

from django.http import JsonResponse

import random

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from asgiref.sync import async_to_sync 
from django.contrib import messages
from .db_orm import create_user, check_repeat_email, login_user, change_password, create_client, client_delete, search_clients, search_clients_with_surname
from .db_orm import add_session_client, session_today, session_today_all_info, get_client_for_id, count_session_client_for_id, delete_for_id_appointment
#import aiohttp
#import threading
from decouple import config
from datetime import datetime
from django.core.mail import send_mail

from django.contrib.auth import logout

def send_verify_code(email):

    code = random.randint(100000, 999999)

    send_mail(
        subject="TattooCRM — Код підтвердження",
        message=f"Вітаємо!\n\nДякуємо за реєстрацію в TattooCRM.\n\nДля підтвердження вашої електронної пошти введіть наступний код:\n\n{code}\n\nКод дійсний протягом 10 хвилин.\n\nЯкщо ви не реєструвалися в TattooCRM, просто проігноруйте цей лист.\n\nЗ повагою,\nКоманда TattooCRM",
        from_email=None,
        recipient_list=[email],
    )

    return code



def send_recovery_code(email):

    code = random.randint(1000000, 9999999)

    send_mail(
        subject = "TattooCRM — Відновлення пароля",
        message=f"Вітаємо!\n\nМи отримали запит на відновлення пароля до вашого облікового запису TattooCRM.\n\nДля підтвердження цієї дії введіть наступний код:\n\n{code}\n\nКод дійсний протягом 10 хвилин.\n\nЯкщо ви не надсилали запит на відновлення пароля, просто проігноруйте цей лист. Ваш акаунт залишиться захищеним.\n\nЗ повагою,\nКоманда TattooCRM\n",
        from_email=None,
        recipient_list=[email],
    )

    return code


def main(request):
    return render(request, 'main.html')










def sign_up(request):
    if request.method == "POST": 
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_repeat = request.POST.get("password_repeat")
        if password == password_repeat:
            email_check = check_repeat_email(email)
            if email_check is True:

                code = send_verify_code(email)

                request.session["signup"] = {
                    "name": name,
                    "email": email,
                    "password": password,
                    "code": code,
                    "created": datetime.now().timestamp(),
                }

                
                return redirect("/sign-up/code/")


            else:
                context = { "error": "Такий користувач уже існує"}
                return render(request, 'sign_up.html', context)

        else:
            context = { "error": "Паролі не збігаються"}
            return render(request, 'sign_up.html', context)

    return render(request, 'sign_up.html')


def sign_up_code(request):
    if request.method == "POST": 
        code = request.POST.get("code")

        data_user = request.session.get("signup")


        if datetime.now().timestamp() - data_user["created"] > 600:
            request.session.pop("signup", None)
            context = { "error": "Вийшов термін дії коду, надішліть знову"}
            return render(request, 'sign_up_code.html', context)
        else:
            if int(data_user["code"]) == int(code):
                user = create_user(data_user["name"], data_user["email"], data_user["password"])
                login(request, user)
                request.session.pop("signup", None)
                return redirect("/profile/")
            else:
                request.session.pop("signup", None)
                context = { "error": "Неправильний код, спробуйте перевірити email"}
                return render(request, 'sign_up_code.html', context)

    return render(request, 'sign_up_code.html')





def sign_in(request):
    if request.method == "POST": 
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = login_user(request, email, password)

        if user != False:
            login(request, user)
            return redirect("/profile/")
        else:
            context = { "error": "Неправильний email або пароль"}
            return render(request, 'sign_in.html', context)
    
    return render(request, 'sign_in.html')
    


def sign_in_password_recovery(request):
    if request.method == "POST": 
        email = request.POST.get("email")
        code = request.POST.get("code")
        password = request.POST.get("password")
        password_repeat = request.POST.get("password_repeat")
        
        if email:
            
            code = send_recovery_code(email)

            request.session["password_recovery"] = {
                "email": email,
                "code": code,
                "created": datetime.now().timestamp(),
            }
            
            
            context = {"code": True}
            return render(request, 'forgot_password.html', context)


        elif code:

            data_user = request.session.get("password_recovery")

            if datetime.now().timestamp() - data_user["created"] > 600:
                request.session.pop("password_recovery", None)
                context = {"email": True, "error": "Вийшов термін дії коду, надішліть знову"}
                return render(request, 'forgot_password.html', context)
            else:
                try:
                    if int(data_user["code"]) == int(code):
                        context = {"password": True}
                        return render(request, 'forgot_password.html', context)
                    else:
                        request.session.pop("password_recovery", None)
                        context = {"email": True, "error": "Неправильний код, спробуйте перевірити email"}
                        return render(request, 'forgot_password.html', context)
                except:
                    ...

            

        elif password:

            data_user = request.session.get("password_recovery")

            if password == password_repeat:
                change_password(data_user["email"], password)
                user = login_user(request, data_user["email"], password)

                if user != False:
                    login(request, user)
                    request.session.pop("password_recovery", None)
                    return redirect("/profile/")
                else:
                    request.session.pop("password_recovery", None)
                    context = {
                        "email": True,
                        "error": "Помилка авторизації."
                    }
                    return render(request, 'forgot_password.html', context)

    context = {"email": True}
    return render(request, 'forgot_password.html', context)
    




    
@login_required
def profile(request):
    print(request.user)
    all_data_session = session_today_all_info(request.user)
    data_session_today = session_today(request.user.clients.all())
    context = {
        "name": request.user.first_name,
        "all_session": data_session_today["all"],
        "completed_session": data_session_today["completed"],
        "scheduled_session": data_session_today["scheduled"],
        "all_data_session": all_data_session
    
    }
    return render(request, 'profile.html', context)
    



def logout_user(request):
    logout(request)
    return redirect("/")


@login_required
def add_client(request):
    if request.method == "POST":
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        telephone = request.POST.get("telephone")
        date_birth = request.POST.get("date_birth") 
        telegram = request.POST.get("telegram")
        email = request.POST.get("email") 
        client_source = request.POST.get("client_source")
        allegria = "allegria" in request.POST

        try:
            create_client(name, surname, telephone, date_birth, telegram, email, client_source, allegria, request.user)
        except:
           return render(request, 'add_client.html', {"error": True})

        return render(request, 'add_client.html', {"successfully": True})


    return render(request, 'add_client.html')





@login_required
def clients(request):
    search = request.GET.get("search")

    if search:
        clients = search_clients(search, request.user)
    else:
        clients = request.user.clients.all()

    context = {
        "clients": clients,
        "clients_count": clients.count()
    }

    return render(request, "clients.html", context)





@login_required
def delete_client(request, id_client):
    if request.method == "POST":
        try:
            client_delete(id_client, request.user)
        except:
            context = {"clients": request.user.clients.all(), "clients_count": len(request.user.clients.all()), "error": True}
            return render(request, 'clients.html', context)


        context = {"clients": request.user.clients.all(), "clients_count": len(request.user.clients.all()), "successfully": True}
        return render(request, 'clients.html', context)

    context = {"clients": request.user.clients.all(), "clients_count": len(request.user.clients.all())}
    return render(request, 'clients.html', context)




@login_required
def new_session(request):
    if request.method == "POST":
        data = request.POST.dict()
        if str(request.POST.get("client_type")) == "existing":
            add_session_client(data['client'], data['date'],data['time'], data['duration'],data['price'], data['service'], data['notes'])
            messages.success(request, "Запис успішно створено!")
            return redirect('new_session')

        elif str(request.POST.get("client_type")) == "new": 
            try:
                allegria = "allegria" in request.POST
                client = create_client(data['name'], data['surname'], data['telephone'], data['date_birth'], data['telegram'], data['email'], data['client_source'], allegria, request.user)
                add_session_client(client.id, data['date'],data['time'], data['duration'],data['price'], data['service'], data['notes'])
                messages.success(request, "Запис та клієнта успішно створено!")

                return redirect('new_session')
            except:
                messages.error(request, "Помилка! Цей користувач уже існує.")
                return redirect('new_session')



    context = {"clients": request.user.clients.all(), "clients_count": len(request.user.clients.all())}
    return render(request, 'new_session.html', context)




@login_required
def clients_search(request):
    search = request.GET.get("q")

    if search:
        clients = search_clients_with_surname(search, request.user)
    else:
        clients = request.user.clients.all()


    return JsonResponse(list(clients.values('id', 'name', 'surname', 'telephone', 'telegram', 'email', 'date_birth', 'allegria', 'client_source', 'created_at', 'whose_client')), safe=False)



@login_required
def appointments_client(request, id_client):
    client = get_client_for_id(id_client, request.user)
    session_client = count_session_client_for_id(id_client, request.user)
    if client != False:
        context = {
            "client": client,
            "appointments_count": session_client.count(),
            "appointments": session_client.all(),

        }
        return render(request, "appointments_client.html", context)
    else:
        return redirect("profile")




@login_required
def appointments_client_delete(request, id_appointment, id_client):
    delete_for_id_appointment(id_appointment)
    return redirect(f"/profile/appointments-client/{id_client}/")
