from django.urls import path, include

from . import views

urlpatterns=[
path('',views.Chat),
path('register',views.AdminRegister.as_view()),
path('login',views.Login.as_view()),
path('code',views.Code)
]