from django import template
from django.utils.safestring import mark_safe
from portal.models import AllocationProduct, ProductPermission, Product

register = template.Library()


@register.filter
def get_value_in_qs(queryset, key):
    if queryset.model == AllocationProduct and key == 'product.id':
        allocated_product_permissions = list(queryset.values('product_permission'))
        allocated_products = []
        for item in allocated_product_permissions:
            if key == 'product.id':
                product_id = ProductPermission.objects.get(pk=item['product_permission']).product.id
                allocated_products.append(product_id)
        return allocated_products
    return mark_safe(list(queryset.values_list(key, flat=True)))


@register.simple_tag
def define(value=None):
    return value


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() or user.is_superuser
