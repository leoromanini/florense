from django import template

register = template.Library()


@register.filter
def get_value_in_qs(queryset, key):
    return list(queryset.values_list(key, flat=True))
