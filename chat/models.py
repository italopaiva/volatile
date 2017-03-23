from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    visibility = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(User, through='UserGroup')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'group')

class Post(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
