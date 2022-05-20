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

        model = load_model('t4s/model/securitycapstone.h5')

        data = np.array(keystroke.split(","), dtype=int)
        data = data * -1
        data = np.array([data])

        result = model.predict(data)

        print('========================================================')
        print('data::\t\t', data)
        print('result::\t', result)
        print('========================================================')

        # 로그인 성공
        if user is not None:
            auth.login(request, user)
            return redirect('t4s:success')

        # 로그인 실패
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


# 모델추가
def addmodel(request):

    if request.method == "POST":

        keystroke = request.POST.get('keystroke')

        data = np.array(keystroke.split(","), dtype=int)
        data = data * -1
        data = np.array([data])

        x_train = data

        print(data)

        try:
            x_train = np.load('t4s/model/x_train.npy')
            print('1')
        except FileNotFoundError:
            np.save('t4s/model/x_train.npy', x_train)
            print('2')

        x_train = np.append(x_train, data, axis=0)
        print(x_train)

        np.save('t4s/model/x_train.npy', x_train)

        return render(request, 't4s/addmodel.html', {'count': x_train.shape})

    else:
        return render(request, 't4s/addmodel.html')
