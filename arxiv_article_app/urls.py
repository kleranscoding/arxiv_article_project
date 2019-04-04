from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('articles', views.get_articles, name='get_articles'),
    path('authors', views.get_authors, name='get_authors'),
]