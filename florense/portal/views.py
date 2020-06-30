from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import json
from .models import *



@login_required
def set_environment(request):
    body = json.loads(request.body)
    request.session['environment'] = body['environment']
    return JsonResponse({'href': '/pedidos'})


@login_required
def environment(request):
    return render(request, 'portal/environment.html')


@login_required
def orders_list(request):
    return render(request, 'portal/orders_list.html')


def order(request):
    return render(request, 'portal/order.html')


def order_existent(request):
    return render(request, 'portal/order_existent.html')


def customers(request):
    return render(request, 'portal/customers_list.html')