
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Email address is required")
        if not username:
            raise ValueError("Username is required")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username = username
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
 

class Post(models.Model):
   description = models.TextField(max_length=100)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   posted = models.DateTimeField(auto_now_add=True)

   def __str__(self):
        return self.name


class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, name='liker')
    post = models.ForeignKey(Post, on_delete=models.CASCADE ,name='post_liked')
 

class Comment(models.Model):
    description = models.TextField(max_length=100)
    user = models.ManyToManyField(User)
    post = models.ManyToManyField(Post)
    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


class Photo(models.Model):
  url = models.CharField(max_length=200)
  post = models.OneToOneField(Post, on_delete=models.CASCADE)
  def __str__(self):
    return f"Photo for post_id: {self.post_id} @{self.url}"


class follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE)