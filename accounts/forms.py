import re
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import Otp


class LoginForm(forms.Form):
    username = forms.CharField(
    widget=forms.TextInput(
    attrs={'class':'form-control text-left',
    "placeholder":"شماره همراه یا ایمیل "
    }))
    password = forms.CharField(
    widget=forms.PasswordInput(
    attrs={'class':'form-control text-left ltr',
           "placeholder":"گذرواژه"
    }))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username:
           raise ValidationError("لطفاً ایمیل یا شماره همراه را وارد کنید.")

        phone_pattern = r"^09\d{9}$"
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if re.match(phone_pattern, username):
            return username

        if re.match(email_pattern, username):
          return username

        raise ValidationError("فرمت وارد شده صحیح نیست. لطفاً ایمیل یا شماره همراه معتبر وارد کنید.")


    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not password:
            raise ValidationError("رمز عبور الزامی است.")

        if len(password) < 8:
            raise ValidationError("رمز عبور باید حداقل ۸ کاراکتر باشد.")
        
        return password


class RegisterForm(forms.Form):
    
    first_name = forms.CharField (
    widget=forms.TextInput(
    attrs={'class': 'form-control text-left',
        'placeholder': 'نام کاربری'
           }

    ))
    phone = forms.CharField (
    widget=forms.TextInput(
    attrs={'class': 'form-control text-left',
           'placeholder': 'شماره تلفن'
        }),
    min_length=11, max_length=11
    )
    
    
    def clean_first_name (self):
        first_name = self.cleaned_data.get('first_name')

        if not first_name:
            raise ValidationError("لطفاً نام را وارد کنید.")

        if not re.match(r'^[آ-یa-zA-Z\s]+$', first_name):
            raise ValidationError("نام فقط می‌تواند شامل حروف باشد.")

        if len(first_name.strip().split()) < 1:
            raise ValidationError("نام معتبر نیست.")

        return first_name
 
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if not last_name:
            raise ValidationError("لطفاً نام خانوادگی را وارد کنید.")

        if not re.match(r'^[آ-یa-zA-Z\s]+$', last_name):
            raise ValidationError("نام خانوادگی فقط می‌تواند شامل حروف باشد.")

        if len(last_name) < 3:
            raise ValidationError("نام خانوادگی باید حداقل 3 حرف باشد.")

        return last_name
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone.isdigit():
            raise ValidationError("شماره تلفن فقط باید شامل ارقام باشد.")

        if not phone.startswith("09"):
            raise ValidationError("شماره تلفن باید با 09 شروع شود.")

        return phone
 


class CheckOtpform(forms.ModelForm):
    code = forms.CharField(
    widget=forms.TextInput(
    attrs={'class': 'w-full drop-shadow-lg outline-none rounded-2xl py-2 text-center'})
    ,max_length=4)

    def clean_code(self):
        code = self.cleaned_data.get('code')

        if not code:
            raise ValidationError("لطفاً کد تأیید را وارد کنید.")

        if not code.isdigit():
            raise ValidationError("کد باید فقط شامل ارقام باشد.")

        if len(code) != 4:
            raise ValidationError("کد باید دقیقاً ۴ رقم باشد.")

        return code
    
    class Meta:
        model = Otp
        fields = ['code']

