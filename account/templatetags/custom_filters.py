# account/templatetags/custom_filters.py
from django import template
from ..models import DynamicValue

register = template.Library()

@register.filter
def get_dynamic_value(student, column):
    try:
        dynamic_value = student.dynamic_values.get(column=column)
        return dynamic_value.get_value()
    except DynamicValue.DoesNotExist:
        return None

