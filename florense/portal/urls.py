from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('ambiente', views.environment, name='environment'),
    path('pedidos', views.orders_list, name='orders_list'),
    path('pedido', views.order, name='order'),
    path('pedido-existente', views.order_existent, name='order'),
    path('clientes', views.customers, name='customers'),
]
