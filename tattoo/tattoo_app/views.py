from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import httpx, asyncio
import json
import requests


from asgiref.sync import async_to_sync 

#import aiohttp
#import threading



def main(request):
    return render(request, 'main.html')

def sign_up(request):
    return render(request, 'sign_up.html')

def sign_in(request):
    return render(request, 'sign_in.html')

def profile(request):
    return render(request, 'profile.html')
    