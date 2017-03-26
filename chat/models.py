from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Group(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='owner',
        on_delete=models.SET_NULL,
        null=True
    )
    members = models.ManyToManyField(
        User,
        related_name='members',
        through='UserGroup'
    )
    visibility = models.BooleanField(_('Public group'), default=True)
    name = models.CharField(_('Group name'), max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def is_private(self):
        return self.visibility == False


class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    pending_confirmation = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'group')

    @classmethod
    def add_user_to_group(cls, user, group_id, pending_confirmation=False):
        group = Group.objects.get(pk=group_id)
        return cls.objects.get_or_create(
            user=user,
            group=group,
            pending_confirmation=pending_confirmation
        )

    @classmethod
    def filter_pending(cls, groups, user, pending=False):
        filtered_groups = []
        for group in groups:
            user_group = UserGroup.objects.get(user=user, group=group)
            if user_group.pending_confirmation is pending:
                filtered_groups.append(group)
        return filtered_groups


class Post(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
