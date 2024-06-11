from django.urls import path
from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('page/<int:page>/', views.main, name='root_paginate'),
    path('author/<str:fullname>/', views.author, name='about_author'),
    path('tag/<str:name>/', views.tag, name='about_tag'),
]