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


@register.filter(name='add_nds')
def add_nds(amount, nds_rate):

    try:
        amount = float(amount)
        print(amount)
        nds_rate = float(nds_rate)
        print(nds_rate)
    except (TypeError, ValueError):
        return amount

    if nds_rate not in (0, -1):
        return amount * (1 + nds_rate / 100)
    return amount
