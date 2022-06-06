from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
import os

from tensorflow.python.keras.models import load_model

from t4s.tf.tf import generate_model, to_np

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
        print(user)

        # 아이디 / 비밀번호 일치
        if user is not None:

            keystroke = request.POST.get('keystroke').strip()
            data = to_np(keystroke)

            model = load_model(f"t4s/model/{user}/{user}.h5")
            result = model.predict(data)

            print('========================================================')
            print('data::\t\t', data)
            print('result::\t', result)
            print('========================================================')

            if result:  # result가 1라면 로그인 실패
                return redirect('t4s:loginfail')

            else:  # result가 0이라면 auth.login으로 로그인 성공 처리
                auth.login(request, user)
                return redirect('t4s:success')

        # 아이디 / 비밀번호 불일치
        else:
            return render(request, 't4s/login.html', {'error': '아이디, 비밀번호 확인'})

    else:
        return render(request, 't4s/login.html')


# 회원가입 페이지
def join(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        password3 = request.POST['password3']
        password4 = request.POST['password4']
        password5 = request.POST['password5']

        keystroke1 = request.POST['keystroke1']
        keystroke2 = request.POST['keystroke2']
        keystroke3 = request.POST['keystroke3']
        keystroke4 = request.POST['keystroke4']
        keystroke5 = request.POST['keystroke5']

        if password1 == password2 == password3 == password4 == password5:
            try:
                User.objects.create_user(username=username, password=password1)
            except IntegrityError:  # ID 중복
                return render(request, 't4s/join.html', {'error': 'ID 중복'})

            # 유저별 h5 파일과 npy 파일을 저장할 폴더 생성.
            if os.path.isdir('t4s/model/' + username) is False:
                os.mkdir('t4s/model/' + username)

            data = to_np(keystroke1)

            # h5 파일 생성 TODO: 입력받은 5개 비밀번호 모두 h5에 적용해야됨. 현재는 1번째 비밀번호만.
            generate_model(data).save(f"t4s/model/{username}/{username}.h5")

            return render(request, 't4s/join.html', {'error': '회원가입 성공'})

        # 비밀번호 오타
        else:
            return render(request, 't4s/join.html', {'error': '비밀번호 확인'})

        # TODO: n번마다 새로 모델링을 하기 위한 카운트 설정. 데이터는 각 유저 폴더에 npy로 저장해 둘 예정

    else:
        return render(request, 't4s/join.html')


# 모델추가
def addmodel(request):
    if request.method == "POST":

        keystroke = request.POST.get('keystroke')
        data = to_np(keystroke)

        try:
            x_train = np.load('t4s/model/x_train.npy')
        except FileNotFoundError:
            x_train = data

        x_train = np.append(x_train, data, axis=0)
        np.save('t4s/model/x_train.npy', x_train)

        return render(request, 't4s/addmodel.html', {'count': x_train.shape})

    else:
        return render(request, 't4s/addmodel.html')
