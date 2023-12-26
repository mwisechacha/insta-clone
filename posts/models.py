from django.conf import settings
from django.db import models
from uuid import uuid4
from .validators import validate_file_size

# Create your models here.
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    caption = models.CharField(max_length=1000)
    posted_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveSmallIntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    
    # def __str__(self) -> str:
    #     return super().__str__()

    def liked_users(self):
        return Like.objects.filter(post=self).values_list('user__username', flat=True)

    class Meta:
        ordering = ['posted_at']

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/images',
                              validators=[validate_file_size])
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.PositiveSmallIntegerField(default=0)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username
    
    class Meta:
        ordering = ['created_at']