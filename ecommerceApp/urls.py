from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.registerPage),
    path('registerAccount', views.register),
    path('register/admin', views.adminRegisterPage),
    path('createAdmin', views.createAdmin),
    path('login', views.login),
    path('home', views.homePage),
    path('logout', views.logout),


    path('createItem', views.createPage),
    path('createProduct', views.createProduct),
    path('product/<int:id>', views.view),
    path('delete/<int:prodId>', views.deleteProduct),
    path('cart', views.cartPage),
    path('addCart/<int:prodId>', views.addToCart),
    path('removeCart/<int:prodId>', views.removeFromCart),
    path('add/<int:prodId>', views.addQuantity),
    path('remove/<int:prodId>', views.removeQuantity),
    path('feature/<int:prodId>', views.featureProduct),
    path('unfeature/<int:prodId>', views.unfeature),
]
