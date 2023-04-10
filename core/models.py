from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images', default='pngwing.com.png')
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self) -> str:
        return self.user.get_username()
    
    
    
class Picturegram(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='posted_images')
    caption = models.TextField()
    time_created = models.DateTimeField(default=datetime.now)
    like_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user
    
    
class PostLikes(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username
    
    
class Follow(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user
    
    