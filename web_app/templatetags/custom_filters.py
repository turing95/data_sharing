from django import template

register = template.Library()

@register.filter(name='get_message_color')
def get_message_color(value):
    colors = {
        "success": "green",
        "error": "red",
        "warning": "yellow",
        "info": "blue",
    }
    return colors.get(value, "gray")