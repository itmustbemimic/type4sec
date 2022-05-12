import logging
import sys

from django.http import HttpResponse
from django.shortcuts import redirect, render

sys.path.append('..')
logging.basicConfig(level=logging.DEBUG)


# login success page
def index(request):
    return HttpResponse("login success!")


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(request.POST)

        return render(request, 't4s/login.html', {'data': 'aaaaa'})

    elif request.method == 'GET':
        return render(request, 't4s/login.html')
