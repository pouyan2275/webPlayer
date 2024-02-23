from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.signupandsignin, name='home'),
    path('signupandsignin/', views.signupandsignin, name='signupandsignin'),
    path('login', views.loginView, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logoutView, name='logout'),
]