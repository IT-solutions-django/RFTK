from django import template

register = template.Library()


@register.filter(name='add_attr')
def add_attr(field, css):
    attrs = {}
    for attr in css.split(','):
        key, value = attr.split('=')
        attrs[key.strip()] = value.strip()

    return field.as_widget(attrs=attrs)


@register.filter
def is_required(field):
    return field.field.required
