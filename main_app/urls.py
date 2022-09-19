from django.urls import path
from . import views

urlpatterns = [
    # General Routes
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    #Posts routes
    path('posts/', views.posts_index, name='post'),
    
    # Signup Route
    path('accounts/sigup/', views.signup, name='signup'),
    # path('accounts/login/', views.login, name='login')
]