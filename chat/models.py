from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    visibility = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(User, through='UserGroup')

class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    content = models.TextField()
