from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.query import QuerySet
from typing_extensions import Self
from typing import Union
from .relationship import Relationship

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, default='profile_pictures/default.jpeg')
    bio = models.TextField()
    pronouns = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)
    following = models.ManyToManyField('self', blank=True, through='core.Relationship', related_name='followers', symmetrical=False)
    # link to another page 


    # creating relationships
    def relates(self, user: Self, status: Union[int, None]=None) -> Relationship:
        if self == user:
            raise Exception('Cannot relate to itself')
        (relation, created) = Relationship.objects.get_or_create(from_user=user, 
                                                      to_user=self,
                                                      defaults={
                                                          'status': status or Relationship.Status.FOLLOWING,
                                                          'from_user': user,
                                                          'to_user': self})
        if not created:
            relation.status = status
            relation.save()
        return relation
    
    def follow(self, user: Self) -> Relationship:
        return self.relates(user, Relationship.Status.FOLLOWING)
    
    def block_user(self, user: Self) -> Relationship:
        return self.relates(user, Relationship.Status.BLOCKED)
    
    def unfollow(self, user: Self) ->  None:
        if self == user:
            raise Exception('A user cannot unfollow itself')
        try:
            relation = Relationship.objects.get(from_user=user, to_user=self)
            relation.delete()
        except User.DoesNotExist:
            raise Exception('Relation not found')
        
    # filter by relationship
    def get_blocked_users(self) -> 'QuerySet[Self]':
        return self.following.filter(
            relationship_from_user__status=Relationship.Status.BLOCKED)
    
    def get_followers(self, include_blocked_user: bool=False) -> 'QuerySet[Self]':
        if include_blocked_user:
            return self.followers.all()
        return self.followers.exclude(
            models.Q(relationship_to_user__status=Relationship.Status.BLOCKED) |
            models.Q(relationship_from_user__in=self.get_blocked_users()))
    
    def get_following(self, include_blocked_user: bool=False) -> 'QuerySet[Self]':
        if include_blocked_user:
            return self.following.all()
        return self.following.exclude(
            models.Q(relationship_to_user__status=Relationship.Status.BLOCKED) |
            models.Q(relationship_from_user__in=self.get_blocked_users()))
    
    def get_friends(self, include_blocked_user: bool=False) -> 'QuerySet[Self]':
        if include_blocked_user:
            return self.followers.filter(
                relationship_from_user__to=self,
                relationship_to_user__by=self)
        return self.followers.filter(
            relationship_from_user__to=self,
            relationship_to_user__by=self,
            relationship_to_user__status=Relationship.Status.FOLLOWING,
            relationship_from_user__status=Relationship.Status.FOLLOWING)
    