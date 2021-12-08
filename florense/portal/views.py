from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import json
from .models import *
from .decorators import environment_required
from django.contrib.auth.models import User
from django.core.mail import get_connection, EmailMultiAlternatives
# from florense.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string


@login_required
def set_environment(request):
    if request.method == 'POST':
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
        id_order = request.POST.get('id_order')
        customer = request.POST.get('customer')
        description = request.POST.get('description')
        number = request.POST.get('number')

        salesmen = User.objects.get(pk=request.POST['salesmen'])
        inspector = User.objects.get(pk=request.POST['inspector'])
        environment = Environment.objects.get(name=request.session.get('environment'))

        if id_order:
            Order.objects.filter(pk=id_order).update(customer=customer, description=description,
                                                          salesmen=salesmen, inspector=inspector,
                                                          environment=environment, number=number)

            order = Order.objects.get(pk=id_order)
        else:
            order = Order(customer=customer, description=description,
                          salesmen=salesmen, inspector=inspector,
                          environment=environment, number=number)
            order.save()

        for value in request.POST.getlist('room'):
            room = Room.objects.get(pk=value)

            # Ignore if this room already included
            if id_order and room in order.rooms.all():
                continue

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
                    if id_order:
                        AllocationLabel.objects.filter(label_permission=permission,
                                                       allocation_room=allocation_room).update(content=value)
                    else:
                        AllocationLabel(label_permission=permission,
                                        allocation_room=allocation_room,
                                        content=value).save()

        for key, value in request.FILES.items():
            if 'product' in key:
                key_splited = key.split('-')
                room = Room.objects.get(pk=key_splited[-2])
                allocation_room = AllocationRoom.objects.get(room=room, order=order)
                product = Product.objects.get(pk=key_splited[-1])
                permission = ProductPermission.objects.get(room=room, product=product)
                if permission:
                    if id_order:
                        allocation_product = AllocationProduct.objects.filter(product_permission=permission,
                                                                              allocation_room=allocation_room).first()
                        allocation_product.image = value
                        allocation_product.save()
                    else:
                        AllocationProduct(product_permission=permission,
                                          allocation_room=allocation_room,
                                          image=value).save()

        return redirect('orders_list')


@environment_required
@login_required
def download_product_image(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        allocation_product = AllocationProduct.objects.get(pk=body['allocationId'])

        if allocation_product:
            filename = allocation_product.image.name.split('/')[-1]
            response = HttpResponse(allocation_product.image, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % filename

            return response


def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None,
                        connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently)
    messages = []
    subject, text, html, from_email, recipient = datatuple
    message = EmailMultiAlternatives(subject, text, from_email, recipient)
    message.attach_alternative(html, 'text/html')
    messages.append(message)
    return connection.send_messages(messages)


@environment_required
@login_required
def approve_allocation_product(request):
    body = json.loads(request.body)
    allocation_product = AllocationProduct.objects.get(pk=body.get('allocationId'))
    if allocation_product and (request.user.groups.filter(name__in=['conferentes', 'gerentes']).exists()
                               or request.user.is_superuser):
        allocation_product.approved = True
        allocation_product.save()

        emails_list = []
        subscribers = User.objects.filter(groups__name__in=['gerentes', 'newsletter'])

        emails_list.append(allocation_product.allocation_room.order.salesmen.email)
        emails_list.append(allocation_product.allocation_room.order.inspector.email)

        for item in subscribers:
            emails_list.append(item.email)

        emails_list = set(emails_list)
        html_message = render_to_string('portal/email.html', {'context': 'values'})
        email_tuple = ('Notificação - Pedido', '', html_message, EMAIL_HOST_USER, emails_list)
        send_mass_html_mail(email_tuple, fail_silently=False)
        return JsonResponse({'status': 'OK'})
