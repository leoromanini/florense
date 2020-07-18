from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("login", auth_views.LoginView.as_view(template_name="portal/login.html",
                                               redirect_authenticated_user=True), name="login",),
    path("logout", auth_views.LogoutView.as_view(), name="logout",),
    path('ambiente', views.environment, name='environment'),
    path('pedidos', views.orders_list, name='orders_list'),
    path('pedido', views.order, name='order'),
    path('pedido/<int:pk>', views.order, name='order-edit'),
    path('clientes', views.customers, name='customers'),

    path('set_environment', views.set_environment, name='set_environment')
]
