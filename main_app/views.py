from tkinter import Variable
from unittest import result
from django.shortcuts import render
import requests


# Create your views here.
def explore(request):
  baseurl = "https://api.unsplash.com/search/photos?"
  key = 'CNdf8VEf5G3eoTB71-GPl6XGzDK4xK1NwCeT4is8qBI'
  variable = request.GET.get('explored')
  image_data = requests.get('{baseurl}query={variable}&client_id={key}'.format(baseurl=baseurl, variable=variable, key=key)).json()
  results = image_data['results']
  return render(request, 'unsplash_api/explore.html', {'results':results})
 

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def posts_index(request):
    return render(request, 'posts/index.html')
