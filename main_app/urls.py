from django.urls import path
from . import views

urlpattern=[
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('posts/', views.posts_index, name='index'),
]