from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import json
from .models import *
from .decorators import environment_required
from django.contrib.auth.models import User


@login_required
def set_environment(request):
    body = json.loads(request.body)
    request.session['environment'] = body['environment']
    return JsonResponse({'href': '/pedidos'})


@login_required
def environment(request):
    return render(request, 'portal/environment.html')


@environment_required
@login_required
def orders_list(request):
    orders = Order.objects.all()
    return render(request, 'portal/orders_list.html', {'orders': orders})


@environment_required
@login_required
def order(request, **kwargs):
    if request.method == 'GET':
        id_order = kwargs.get('pk')
        if id_order:
            order = Order.objects.get(pk=id_order)
        else:
            order = None
        rooms = Room.objects.all()
        salesmen = User.objects.filter(groups__name='vendedores')
        inspector = User.objects.filter(groups__name='conferentes')
        if order:
            allocation_rooms = AllocationRoom.objects.filter(order=order)
            return render(request, 'portal/order.html', {'order': order, 'allocation_rooms': allocation_rooms,
                                                           'rooms': rooms, 'salesmen': salesmen, 'inspector': inspector})
        else:
            return render(request, 'portal/order.html', {'rooms': rooms, 'salesmen': salesmen, 'inspector': inspector})

    if request.method == 'POST':
        customer = request.POST['customer']
        description = request.POST['description']
        number = request.POST['number']

        salesmen = User.objects.get(pk=request.POST['salesmen'])
        inspector = User.objects.get(pk=request.POST['inspector'])
        environment = Environment.objects.get(name=request.session.get('environment'))

        order = Order(customer=customer, description=description,
                      salesmen=salesmen, inspector=inspector,
                      environment=environment, number=number)

        order.save()

        for value in request.POST.getlist('room'):
            room = Room.objects.get(pk=value)
            allocation = AllocationRoom(order=order, room=room)
            allocation.save()

        for key, value in request.POST.items():
            if 'label' in key:
                key_splited = key.split('-')
                room = Room.objects.get(pk=key_splited[-2])
                allocation_room = AllocationRoom.objects.get(room=room, order=order)
                label = Label.objects.get(pk=key_splited[-1])
                permission = LabelPermission.objects.get(room=room, label=label)
                if permission:
                    allocation_label = AllocationLabel(label_permission=permission,
                                                       allocation_room=allocation_room,
                                                       content=value)
                    allocation_label.save()

        for key, value in request.FILES.items():
            if 'product' in key:
                key_splited = key.split('-')
                room = Room.objects.get(pk=key_splited[-2])
                allocation_room = AllocationRoom.objects.get(room=room, order=order)
                product = Product.objects.get(pk=key_splited[-1])
                permission = ProductPermission.objects.get(room=room, product=product)
                if permission:

                    allocation_product = AllocationProduct(product_permission=permission,
                                                           allocation_room=allocation_room,
                                                           image=value)

                    allocation_product.save()

        return redirect('orders_list')


def order_existent(request):
    return render(request, 'portal/order_existent.html')


def customers(request):
    return render(request, 'portal/customers_list.html')
