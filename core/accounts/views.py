from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import time
from datetime import datetime
from .tasks import sendEmail

# Create your views here.

def send_email(request):
    sendEmail.delay()
    return HttpResponse('Email Sended')

def test(reqeust):

    if cache.get("test_data_delay") is None:
        time.sleep(5)
        cache.set("test_data_delay", datetime.now().strftime("%Y /%M /%d %H : %m"),60)
    return JsonResponse({"data":cache.get("test_data_delay")})

