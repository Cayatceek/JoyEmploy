from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    """
    Разбивает строку на части по указанному разделителю.
    Использование: {{ string|split:"delimiter" }}
    """
    if not isinstance(value, str):
        return value
    return value.split(delimiter)