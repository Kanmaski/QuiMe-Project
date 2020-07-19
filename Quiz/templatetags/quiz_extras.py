from django import template

register = template.Library()

@register.filter
def mydictcustom(mydict, key):
    return mydict[key]

@register.filter
def percentage(value):
    return format(value, ".2%")

