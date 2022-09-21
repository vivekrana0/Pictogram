from .models import Follow, Post, User, Like, Comment
from django.shortcuts import render, redirect
from .forms import UserCreationForm, PostForm
from django.contrib.auth import login
from django.views.generic import DeleteView, UpdateView

import uuid
import boto3
import requests

S3_BASE_URL = 'https://s3.ca-central-1.amazonaws.com/'
BUCKET = 'pictogramsei53'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def posts_index(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'posts/index.html',{ 'posts': posts})

def posts_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.all()
    return render(request, 'posts/detail.html', {'post': post,'comments': comments })

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid Input'
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form, 'error_message': error_message})


def addpost(request):
    user = request.user.id
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            photo_file = request.FILES.get('photo-file', None)
            if photo_file:
                s3 = boto3.client('s3')
                key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
                try:
                    s3.upload_fileobj(photo_file, BUCKET, key)
                    url = f"{S3_BASE_URL}{BUCKET}/{key}"
                    new_post = form.save(commit=False)
                    new_post.user_id = user 
                    new_post.photo = url  
                    new_post.save()      
                except:
                    print('An error occurred uploading file to S3')
    else:
        form = PostForm()
        return render(request, 'posts/addpost.html', {'form': form})
    return redirect('post')

class PostDelete(DeleteView):
    model = Post
    success_url = '/posts/'

class PostUpdate(UpdateView):
    model = Post
    fields = ['description']

def likes(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    likes = post.likes
    check_ifliked = Like.objects.filter(liker=user, post_liked=post).count()
    if check_ifliked:
        Like.objects.filter(liker=user, post_liked=post_id).delete()
        likes = likes - 1
    else:
        Like.objects.create(liker=user, post_liked=post)
        likes = likes + 1
    post.likes = likes
    post.save()
    print(likes)
    return redirect('detail', post_id=post_id)

def explore(request):
  baseurl = "https://api.unsplash.com/search/photos?"
  key = 'CNdf8VEf5G3eoTB71-GPl6XGzDK4xK1NwCeT4is8qBI'
  variable = request.GET.get('explored')
  image_data = requests.get('{baseurl}query={variable}&client_id={key}'.format(baseurl=baseurl, variable=variable, key=key)).json()
  results = image_data['results']
  return render(request, 'unsplash_api/explore.html', {'results':results})

def profile(request, user_id):
    user = User.objects.get(id=user_id)
    user_id = user.id
    posts = Post.objects.filter(user = user_id)
    posts_count = posts.count()
    following = Follow.objects.filter(following=user).count()
    followers = Follow.objects.filter(follower=user).count()
    is_following = Follow.objects.filter(following = request.user, follower = user).exists()
    return render(request, 'profile.html',{'posts':posts, 'profile_user': user, 'profile_user_id': user_id, 'following': following, 'followers': followers, 'posts_count': posts_count, 'is_following': is_following})

def search(request, user):
    # user = request.GET.get('username')
    profile = User.objects.get(username=user)
    user_id = profile.id
    return redirect('profile', user_id=user_id)

def follow(request, profile_user_id):
    profile_user = User.objects.get(id=profile_user_id)
    is_following = Follow.objects.filter(following = request.user, follower = profile_user).exists()
    if is_following:
        Follow.objects.filter(following = request.user, follower = profile_user).delete()
    else:
        Follow.objects.create(following = request.user, follower = profile_user)
    return redirect('profile', user_id=profile_user_id )