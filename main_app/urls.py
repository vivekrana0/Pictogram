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
    
    # Post Routes
    path('posts/add_post/', views.addpost, name='add_post'),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='delete'),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='update'),

    # Like logic
    path('posts/<int:post_id>/like/', views.likes, name='like'),

    # Api route
    path('unsplash_api/explore/', views.explore, name='explore'),

    # Profile Route
    path('profile/<int:user_id>/', views.profile, name='profile'),

    # Search Route
    path('search/profile/', views.search, name='search'),
    
    # Follow Logic
    path('search/follow/<int:profile_user_id>/', views.follow, name='follow'),

    #comment route
    path('posts/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/delete_comment/', views.delete_comment, name='delete_comment'),
    path('post/<int:pk>/update/', views.CommentUpdate.as_view(), name='comment_update'),

    # Feed Logic
    path('feed/', views.feed, name='feed'),
]