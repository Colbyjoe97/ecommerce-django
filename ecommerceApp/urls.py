from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.registerPage),
    path('registerAccount', views.register),
    path('adminRegister', views.adminRegisterPage),
    path('createAdmin', views.createAdmin),
    path('login', views.login),
    path('home', views.success),
    path('createItem', views.createPage),
    path('createProduct', views.createProduct),
    path('logout', views.logout),
]
