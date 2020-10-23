from django import template
import calendar

register = template.Library()


@register.filter
def subtract(value, arg):
    return int(value) - int(arg)



@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]



@register.filter
def multiplication(value, arg):
    return round(float(value) * float(arg), 2)