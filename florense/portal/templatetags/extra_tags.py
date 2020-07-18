from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def get_value_in_qs(queryset, key):
    return mark_safe(list(queryset.values_list(key, flat=True)))


@register.simple_tag
def define(value=None):
  return value
