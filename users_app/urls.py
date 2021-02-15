from django.urls import path,include
from users_app import views as users_view
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('register', users_view.register,name='register'),
    path('login', auth_view.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout', auth_view.LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('',users_view.account, name='account'),
    #path('contact',users_view.contact, name='contact'),
]