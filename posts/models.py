from django.contrib.auth.models import User
from django.db import models
from uuid import uuid4
from .validators import validate_file_size

# Create your models here.
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    caption = models.CharField(max_length=1000)
    posted_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveSmallIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # def __str__(self) -> str:
    #     return super().__str__()

    class Meta:
        ordering = ['posted_at']

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/images',
                              validators=[validate_file_size])
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Follow(models.Model):
    followers = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user
    
    class Meta:
        ordering = ['created_at']