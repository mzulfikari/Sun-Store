from django.urls import path,include
from . import views



app_name = 'accounts'

urlpatterns = [
    path('login/',views.LoginViews.as_view(),name="login"),
    path('register/',views.RegisterViews.as_view(),name="register"),
]
