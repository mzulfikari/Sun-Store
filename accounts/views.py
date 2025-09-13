from django.shortcuts import render,redirect
from django.contrib.auth import views as auth_views
from django.views import View
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.views.generic import TemplateView

class LoginViews(View):
    """
    Checking the login system through the phone number as the main key or email and password
    """
    def get (self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = LoginForm()
        return render(request,'accounts/login.html',{'form':form})
    
    def post(self,request):
        form = LoginForm(request.POST)
        errors = []
        if form.is_valid():
            valid = form.cleaned_data
            login_users = authenticate(username=valid['username'],password=valid['password'])
            if login_users is not None:
                login(request,login_users)
                return redirect('/')
            else:
                errors.append("اطلاعات وارد شده صحیح نمی باشد")
        else:
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(error)
        
        return render(request,'accounts/login.html',{
            'form':form,
            'errors': errors
            })       
    
    
class RegisterViews(TemplateView):
    template_name = 'accounts/register.html'
  
   
class LogoutViews(auth_views.LogoutView):
    
    pass