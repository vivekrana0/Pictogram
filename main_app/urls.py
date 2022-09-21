from django.urls import path
from . import views

urlpatterns = [
    # General Routes
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    #Posts routes
    path('posts/', views.posts_index, name='post'),
    path('posts/<int:post_id>/', views.posts_detail, name='detail'),
    
    # Signup Route
    path('accounts/sigup/', views.signup, name='signup'),

    # path('cats/<int:cat_id>/add_photo/', views.add_photo, name='add_photo'),

    path('posts/add_post', views.addpost, name='add_post'),
]