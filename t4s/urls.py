from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "t4s"
urlpatterns = [
    path('test/', views.login, name='login2'),
    path('success/', views.index, name='success'),
    path('', auth_views.LoginView.as_view(template_name='t4s/login.html'), name='login')
]
