from django.http import HttpResponse
from django.shortcuts import render
import sys
import keyboard
import time

sys.path.append('..')


# Create your views here.
def index(request):
    return HttpResponse("login success!")
