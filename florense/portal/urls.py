from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('ambiente', views.environment, name='environment'),
    path('pedidos', views.orders, name='pedidos'),
]