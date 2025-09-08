import re
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError



class LoginForm(forms.Form):
    username = forms.CharField(
    widget=forms.TextInput(
    attrs={'class':'form-control text-left',
    "placeholder":"شماره همراه یا ایمیل "
    }))
    password = forms.CharField(
    widget=forms.PasswordInput(
    attrs={'class':'form-control text-left ltr'
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
