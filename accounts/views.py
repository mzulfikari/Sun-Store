from django.shortcuts import render
from django.contrib.auth import views as auth_views



class LoginViews(auth_views.LoginView):
    
   
class LogoutViews(auth_views.LogoutView):
    pass