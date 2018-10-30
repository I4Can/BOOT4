from django import template
register=template.Library()

@register.simple_tag()
def intfy(string,num):
    if int(string)>num:
        return int(string)