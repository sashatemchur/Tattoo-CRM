from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import httpx, asyncio
import json
import requests

import random

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from asgiref.sync import async_to_sync 

from .db_orm import create_user, check_repeat_email, login_user
#import aiohttp
#import threading
from decouple import config
from datetime import datetime
from django.core.mail import send_mail


def send_verify_code(email):

    code = random.randint(100000, 999999)

    send_mail(
        subject="TattooCRM — Код підтвердження",
        message=f"Вітаємо!\n\nДякуємо за реєстрацію в TattooCRM.\n\nДля підтвердження вашої електронної пошти введіть наступний код:\n\n{code}\n\nКод дійсний протягом 10 хвилин.\n\nЯкщо ви не реєструвалися в TattooCRM, просто проігноруйте цей лист.\n\nЗ повагою,\nКоманда TattooCRM",
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
            del request.session["signup"]
            context = { "error": "Вийшов термін дії коду, надішліть знову"}
            return render(request, 'sign_up_code.html', context)
        else:
            if int(data_user["code"]) == int(code):
                user = create_user(data_user["name"], data_user["email"], data_user["password"])
                login(request, user)
                del request.session["signup"]
                return redirect("/profile/")
            else:
                del request.session["signup"]
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
    
@login_required
def profile(request):
    print(request.user)
    context = {"name": request.user.first_name}
    return render(request, 'profile.html', context)
    