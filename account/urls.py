from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('products/', views.products, name="products"),
    path('customer/',views.customer, name="customer"),
]
