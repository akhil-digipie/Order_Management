from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),

    path('customer/<str:id>/',views.customer, name="customer"),
    path('view_customer_list/',views.view_customer_list, name="view_customer_list"),
    path('create_order/<str:id>/',views.createOrder, name="create_order"),
    path('update_form/<str:id>/', views.updateOrder, name="update_form"),
    path('delete_form/<str:id>/', views.deleteOrder, name="delete_form"),
]
