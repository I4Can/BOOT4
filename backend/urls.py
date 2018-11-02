from django.urls import path
from .views import *
urlpatterns=[
    path('',backend),
    path('delArticle/',delArticle),
    path('add_article/',add_article),
    path('edit_article/',edit_article),
    path('sort_article/',sort_Article),
    path('message/',message),
    path('media/',media),
]