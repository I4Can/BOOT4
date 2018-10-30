"""MyBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from .views import *
from web import views
from django.conf.urls import url
from repository import tests

from django.views.static import serve
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home),
    path('home/',home),
    path('sign/',views.sign),
    path('register/',views.register),
    path('message/',views.message),
    path('check_username/',check_username),
    path('jottings/',views.jottings),
    path('about/',views.about),
    path('recall/',views.recall),
    path('share/',views.share),
    path('like/',views.like),
    path('receive_comment/',views.receive_comment),
    re_path(r'^blog/(?P<article_id>[\d]+)'+'.html',views.show_article),
    path('status/',views.status),
    path('backend/',include("backend.urls")),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': 'media'}),
    path('test/',test),
    path('edit_info/',edit_info),
]
