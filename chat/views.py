from django.shortcuts import render
from chat.forms import NewUserForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import View
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from chat.models import Group, UserGroup, Post


def home(request):
    return TemplateResponse(request, 'home.html')

class SignUp(View):

    form = NewUserForm

    def get(self, request):
        context = {'form': self.form()}
        return TemplateResponse(request, 'signup.html', context)

    def post(self, request):

        form = self.form(data=request.POST)

        if form.is_valid():
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            response = HttpResponseRedirect(reverse('login'))
            msg_level = messages.SUCCESS
            msg = _('Registered with success!')
            messages.add_message(request, msg_level, msg)
        else:
            context = {'form': form}
            response = TemplateResponse(request, 'signup.html', context)

        return response

class ListGroups(View):

    @method_decorator(login_required)
    def get(self, request):
        public_groups = Group.objects.filter(visibility=True).exclude(members__pk=request.user.pk)
        user_groups = Group.objects.filter(members__pk=request.user.pk)
        context = {'public_groups': public_groups, 'user_groups': user_groups}
        return TemplateResponse(request, 'groups/list.html', context)


class GroupChat(View):

    @method_decorator(login_required)
    def get(self, request, group_id):
        group = Group.objects.get(pk=group_id)
        user_group = UserGroup.objects.get(group=group)
        posts = Post.objects.filter(group=user_group)
        context = {
            'posts': posts,
            'group': group
        }
        return TemplateResponse(request, 'posts/list.html', context)


@login_required
def join_group(request, group_id):
    group = Group.objects.get(pk=group_id)
    user_group, created = UserGroup.objects.get_or_create(
        user=request.user,
        group=group
    )
    msg_level = messages.SUCCESS if created else messages.WARNING
    msg = _('Congrats! You have joined the group %s.' % group.name) if created \
        else _('You are already in group %s.' % group.name)
    messages.add_message(request, msg_level, msg)
    return HttpResponseRedirect(reverse('group_chat'))
