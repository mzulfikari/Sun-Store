from django.shortcuts import render,redirect
from django.contrib.auth import views as auth_views
from django.views import View
from django.contrib.auth import authenticate, login
from .forms import LoginForm



class LoginViews(View):
    
    def get (self, request):
        form = LoginForm()
        return render(request,'accounts/login.html',{'form':form})
    
    def post(self,request):
        form = LoginForm()
        if form.is_valid():
            valid = form.cleaned_data
            login_users = authenticate(username=valid['username'],password=valid['password'])
            if login_users is not None:
                login(request,login_users)
                return redirect('')
            else:
                form.add_error("username", "اطلاعات وارد شده صحیح نمی باشد")
        else:
            form.add_error("username","لطفا دوباره بررسی کنید اطلاعات وارد شده صحیح نمی باشد")
        
        return render(request,'accounts/login.html',{'form':form})       
    
    
   
class LogoutViews(auth_views.LogoutView):
    pass