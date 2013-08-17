from django import template

register = template.Library()

# settings value
@register.filter
def sum_month_cnt(list):
    res = 0
    for x in list:
        res += len(x)
    return res