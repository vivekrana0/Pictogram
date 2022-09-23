# Project 3: Django Full-Stack Application
![Banner](main_app/static/img/logo-2.png)
<br>

## Introduction

In the year of 2022, it is a common sight to see individuals using a social media application on a electronic device of their choice. Examples of these social media apps are:

- Instagram
- Facebook
- Twitter
- TikTok
- LinkedIn

Welcome to Pictogram, an Instagram clone created using Django, PostgreSQL and styled with Bootstrap. Instagram is photo and video sharing application where users can view, add, delete, and comment on other user's posts.

Pictogram will have similar functionalities and uses an API to replicate the explore functionality found on Instagram. Please take a look at Pictogram and enjoy the features available!
<br>

## Tech Stack

- <b>Django</b>
- <b>PostgreSQL</b>
- <b>Bootstrap</b>
- <b>Amazon Web Services (AWS S3)</b>
- <b>Unsplash API</b>

## Getting Started

Lets get started!
Access the app through the link below:
### [Live Link](https://pictogram-webapp.herokuapp.com/)

## Features

### Home Page
<img src='https://imgur.com/Shnayjs.png'>

### Create New Post Template
<img src='https://imgur.com/Zvr3NdE.png'>

### Unsplash API:

The Unsplash API provids us with over 3 million free high-resolution images that are brought to us by the world’s most generous community of photographers.
Our app uses the Usplah Api to provide the users with the ability to search through and locate the perfect image to use for their post.

<img src='https://i.imgur.com/mhy1mdv.png'>

### Post details:
Our App users can edit and update their own posts. Users can make a comment, delete their own comments, give a like, and cancel the like that was given. 

<table>
  <tr>
    <td>My Post Page</td>
     <td>Other user's post page</td>
  </tr>
  <tr>
    <td><img src="https://imgur.com/1ayZ645.png" width=300 height=330></td>
    <td><img src="https://imgur.com/6GfXLUm.png" width=300 height=330></td>
  </tr>
 </table>

### My profile:
Every user has a profile that record all their posts, and it also stores the values that counts the number of posts, the number of followings, and the number of followers. From other users' profile information, we can see a following/unfollow button.

<table>
  <tr>
    <td>My profile info</td>
     <td>Other user's profile info</td>
  </tr>
  <tr>
    <td><img src="https://imgur.com/DjHvJ1f.png" width=200 height=80></td>
    <td><img src="https://imgur.com/wN6BPKX.png" width=200 height=80></td>
  </tr>
 </table>

## Code Examples

- The code snippet below is used to implement pulling 30 different images from the API Unsplash and adding them to the explore template.

```
def explore(request):
  baseurl = "https://api.unsplash.com/search/photos?"
  key = 'CNdf8VEf5G3eoTB71-GPl6XGzDK4xK1NwCeT4is8qBI'
  variable = request.GET.get('explored')
  image_data = requests.get('{baseurl}per_page=30&query={variable}&client_id={key}'.format(baseurl=baseurl, variable=variable, key=key)).json()
  results = image_data['results']
  return render(request, 'unsplash_api/explore.html', {'results':results})
```
- The code snippet below is used to determine if a post has been liked by a specific user. This function also provides the count of likes per post and is used in the detail template.

```
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
```

## Future enhancements

1. Create a modal option for the login screen
2. Create and update the search bar to have more dynamic options
3. Option for users to add a bio and avatar/profile picture
4. Profile can be set to private, so only followers can see your profile.
5. Upload more than one picture for each post.

## Project Tools

### [Trello Board](https://trello.com/b/G8PbOsoL/sei-project-3)
### [Wireframes](https://www.figma.com/file/fnicF6E5dx9rpEh1OykUjT/Pictogram?node-id=0%3A1)
### [ERD](https://app.genmymodel.com/api/repository/lc9900/Instagram)

## Team Members

[Edwin Hawk Yu](https://github.com/EdwinHawkYu)

[Wasim Okadia](https://github.com/Wasimoak)

[Ruoyi Chen](https://github.com/xtal00)

[Vivek Rana](https://github.com/vivekrana0)
