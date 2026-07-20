from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Return the value for a given key in a dictionary."""
    return dictionary.get(key)