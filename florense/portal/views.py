from django.shortcuts import render


def login(request):
    return render(request, 'portal/login.html')


def environment(request):
    return render(request, 'portal/environment.html')


def orders_list(request):
    return render(request, 'portal/orders_list.html')


def order(request):
    return render(request, 'portal/order.html')


def order_existent(request):
    return render(request, 'portal/order_existent.html')

def customers(request):
    return render(request, 'portal/customers_list.html')
