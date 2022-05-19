import os

import numpy
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import auth
from tensorflow.python.keras.models import load_model

import numpy as np


# login success page
def index(request):
    return HttpResponse("login success!")


# 로그인 페이지
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)

        keystroke = request.POST.get('keystroke')

        model = load_model('t4s/securitycapstone.h5')
        data = np.array(keystroke.split(","), dtype=int)
        data = data*-1
        data = np.array([data])
        result = model.predict(data)

        print(data.shape)
        print(data)
        print(result)

        if user is not None:
            auth.login(request, user)
            return redirect('t4s:success')
        else:
            return render(request, 't4s/login.html', {'error': '로그인 실패'})

    else:
        return render(request, 't4s/login.html')


# 회원가입 페이지
def join(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        print(request.POST)
        return render(request, 't4s/join.html')

    else:
        return render(request, 't4s/join.html')
