# organizacao/templatetags/extra_filters.py
from django import template

register = template.Library()

@register.filter
def attr(obj, attr_name):
    if '.' in attr_name:
        attrs = attr_name.split('.')
        for a in attrs:
            obj = getattr(obj, a, None) or (obj.get(a) if isinstance(obj, dict) else None)
            if obj is None:
                return ''
        return obj
    try:
        return getattr(obj, attr_name)
    except AttributeError:
        if isinstance(obj, dict):
            return obj.get(attr_name, '')
        return ''

@register.filter
def split(value, sep=','):
    """Divide uma string pelo separador informado. Ex: {{ string|split:',' }}"""
    if not value:
        return []
    return value.split(sep)

@register.filter
def get_item(dictionary, key):
    """Acessa dictionary[key] no template."""
    return dictionary.get(key)