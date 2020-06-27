from django.shortcuts import render


def login(request):
    return render(request, 'portal/login.html')


def environment(request):
    return render(request, 'portal/environment.html')


def orders(request):
    return render(request, 'portal/orders.html')
