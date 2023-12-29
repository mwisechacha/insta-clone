from django.conf import settings
from django.db import models



# define the status of the relationship
class Status(models.IntegerChoices):
    BLOCKED = 0, 'Blocked'
    FOLLOWING = 1, 'Following'

class Relationship(models.Model):

    class Meta:
        verbose_name = 'Relationship'
        verbose_name_plural = 'Relationships'

    Status = Status

    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE) # who started the following
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE) # who is being followed

    @property
    def name(self) -> str:
        return f'Relationship from {self.from_user} to {self.to_user}'
    
