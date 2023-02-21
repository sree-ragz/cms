from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index,name='home'),
    path('register/',views.register,name='register'),
    path('register2/',views.register2,name='register2'),
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logoutpage,name='logout'),
    path('token/',views.token_sent,name='token_sent'),
    path('verify/<uid>',views.verify,name='verify'),
    # path('settings/',views.Editprofile.as_view(),name='settings'),
]
