from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('signin/',views.signin, name='signin'),
    path('signup/',views.signup, name='signup'),
    path('logout/',views.logout_),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('delete_msg/',views.delMsg, name='delMsg')
]