from .models import Post, User, Like
from django.shortcuts import render, redirect
from .forms import UserCreationForm, PostForm
from django.contrib.auth import login
from django.views.generic import DeleteView, UpdateView

import uuid
import boto3

S3_BASE_URL = 'https://s3.ca-central-1.amazonaws.com/'
BUCKET = 'pictogramsei53'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def posts_index(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'posts/index.html',{ 'posts': posts })

def posts_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'posts/detail.html', {'post': post })

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