from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'basicapp'

urlpatterns  = [
    path("",views.index,name='index'),
    path("register",views.register, name="register"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("fare",views.fare,name="fare"),
    path('farecal',views.farecal,name="farecal"),
    path('rent_now',views.rent_now,name="rent_now"),
    path('contact',views.contact,name='contact'),
    path('mybookings',views.mybookings,name='mybookings')
]