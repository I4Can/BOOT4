from django.test import TestCase
from repository import models
from django.shortcuts import HttpResponse
# Create your tests here.

def add_data(request):
    for i in range(1,90):
        # models.Article.objects.filter(id=i).delete()
        models.Article.objects.create(title='标题'+str(i),brief="这个错误直接翻译过来就是，重复的字段'card'",illustration="dragon.jpg",category_id=2,like=0)
    return HttpResponse('OK')