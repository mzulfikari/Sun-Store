from django.urls import path,include
from . import views


app_name = "website"

urlpatterns = [  
    path('',views.IndexViews.as_view(),name="Index"),

]