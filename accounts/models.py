from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator


class UserType(models.IntegerChoices):
    """
    Type users
    """
    superuser = 1,_('superuser')
    admin = 2,_('admin')
    customer = 3,_('customer')



class UserManager(BaseUserManager):
    """
    Custom user model manager where phone is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, phone, password=None, first_name=None, last_name=None, **extra_fields):

        if not phone:
            raise ValueError("لطفا شماره تلفن را وارد کنید")

        user = self.model(
            phone=phone,password=password,**extra_fields
        )

        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, phone, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given phone and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("type", UserType.superuser.value)
        
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(phone, password, **extra_fields)

       

class User(AbstractBaseUser,PermissionsMixin):
    
    phone = models.CharField(
        unique=True,verbose_name=_('شماره تلفن'),max_length=15
        )
    is_staff = models.BooleanField(
        default=False
    )
    is_active = models.BooleanField(
        default=False
    )
    is_verified = models.BooleanField(
        default=False
    )
    type = models.ImageField(
        choices=UserType.choices,default=UserType.customer.value,verbose_name= _('نقش کاربر')
    )
    created_dete = models.DateTimeField(
        auto_created=True,verbose_name=_('تاریخ ایجاد '),
    )
    update_date = models.DateTimeField(
      verbose_name= _(' تاریخ بروز رسانی'),auto_now=True
    )
    
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []
    
    
    objects = UserManager()
    
    def __str__(self):
        return self.phone



class Profile (models.Model):
    user = models.OneToOneField(
        'User',on_delete=models.CASCADE,related_name='user_profile'
        )
    first_name = models.CharField(
        max_length=50, verbose_name= _('نام ')
        )
    last_name = models.CharField(
        max_length=50, verbose_name= _(' نام خانوداگی ')
        )
    email = models.EmailField(
        verbose_name=_('ایمیل'),null=True,blank=True
        )
    image = models.ImageField(
        upload_to="profile",null=True, blank=True,verbose_name= _('تصویر پروفایل')
    )
    created_dete = models.DateTimeField(
        auto_created=True,verbose_name=_('تاریخ ایجاد '),
    )
    update_date = models.DateTimeField(
        auto_now=True,verbose_name= _(' تاریخ بروز رسانی')
    )