from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Article)
admin.site.register(Article_detail)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(userInfo)
admin.site.register(Category)


