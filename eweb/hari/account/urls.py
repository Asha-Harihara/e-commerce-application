from django import views
from django.urls import path, include
from . import views

urlpatterns = [
    path('register/',views.registerPage, name="register" ),
    path('login/',views.loginPage, name="login" ),
    path('', views.home, name="home"),
    path('logout/', views.logoutUser, name="logout"),
    path('buyhome/', views.buyhome, name="buyhome"),
    path('sellhome/', views.sellhome, name="sellhome"),
    path('cart/', views.cart, name="cart"),
    path('orders/', views.orders, name="orders"),
    path('update_item/', views.updateItem, name="update_item"),
    path('checkout/', views.checkout, name="checkout"),
    path('orderItems/', views.orderItems, name="orderItems"),
    path('viewurprod/', views.viewurprod, name="viewurprod"),
    path('update_quant/', views.updateQuant, name="update_quant"),
    path('viewurorder/', views.viewurorder, name="viewurorder"),
    path('update_status/', views.updateStatus, name="update_status"),
    path('addproduct/', views.addproduct, name="addproduct"),
]