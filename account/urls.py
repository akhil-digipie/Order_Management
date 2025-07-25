from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('products/', views.products, name="products"),
    path('customer/<str:id>/',views.customer, name="customer"),
    path('view_customer_list/',views.view_customer_list, name="view_customer_list"),
]
