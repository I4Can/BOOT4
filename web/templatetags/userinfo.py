from repository import models
from django import template

register = template.Library()
@register.filter
def getInfo(username):
    user=models.userInfo.objects.filter(username=username).first()
    return user