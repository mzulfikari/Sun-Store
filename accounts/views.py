from random import randint
from uuid import uuid4
from django.shortcuts import render,redirect
from django.contrib.auth import views as auth_views
from django.views import View
from django.contrib.auth import authenticate, login
from accounts.admin import User
from .forms import CheckOtpform, LoginForm
from django.views.generic import TemplateView
from.forms import Otp,RegisterForm
from django.urls import reverse



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
    
    
class RegisterView(View):
    """User login through phone number and email"""

    def get (self,request):
        form = RegisterForm()
        return render (request,'accounts/register.html',{'form':form})

    def post(self,request):
        phone = request.POST.get('phone')
        form = RegisterForm(request.POST)
        if form.is_valid():
          
            valid = form.cleaned_data
            randcode = randint(1000,9999)
            #دریافت رمز یکبار مصرف
            # sms_api.verification({
            #     'receptor':valid["phone"],'type':'1','template':'randcode','param1':randcode
            # })
            token = str(uuid4())
            request.session['phone'] = valid['phone']
            Otp.objects.create(phone=valid['phone'],code=randcode,token=token)
            return redirect(reverse('accounts:otp') + f'?token={token}')
        else:
            form.add_error('phone', "اطلاعات وارد شده صحیح نمی باشد")
        return render(request, "accounts/register.html",{'form': form,})


class CheckOtp(View):
    """
    To authenticate the entered number and expire
    the one-time code within 2 minutes
    """

    def get(self, request):
        form = CheckOtpform()
        phone = request.session.get('phone') 
        return render(request, 'accounts/otp.html',{'form': form,'phone': phone})


    def post(self,request):
        token = request.GET.get('token')
        form = CheckOtpform(request.POST)

        if form.is_valid():
            valid = form.cleaned_data
            if Otp.objects.filter(code=valid['code'],
             token=token,).exists():otp = Otp.objects.get(token=token)
                  
            if not otp:
                form.add_error('code', "کد اشتباه است")
                return render(request, 'accounts/otp.html', {'form': form})

            user , is_created = User.objects.get_or_create(phone=otp.phone,)
            if is_created:
                user.first_name = valid.get('first_name')
                user.last_name = valid.get('last_name')
                user.save()      
            otp.delete()
            request.session.pop('phone', None) 
            login(request,user,backend="django.contrib.auth.backends.ModelBackend")
            
            return redirect('/')

        else:
             form.add_error(None, "اطلاعات وارد شده صحیح نمی باشد ")

        return render(request,'accounts/otp.html',{'form':form })
   
   
   
class LogoutViews(auth_views.LogoutView):
    """
    Logot 
    """
    pass