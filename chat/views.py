from chat.forms import NewUserForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import View
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from chat.models import Group, UserGroup, Post
from chat.forms import NewPostForm, NewGroupForm


def home(request):
    """ Displays the homepage """
    return TemplateResponse(request, 'home.html')


class SignUp(View):
    form = NewUserForm

    def get(self, request):
        """ Return sign up template """
        context = {'form': self.form()}
        return TemplateResponse(request, 'signup.html', context)

    def post(self, request):
        """
        Register a new user if the given data is right
        and then redirect to login.

        If the data does not pass validation it stays on sign up page
        """
        form = self.form(data=request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password']
            )
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
        """  Get all public groups and current user groups and display """
        public_groups = Group.objects \
            .filter(visibility=True) \
            .exclude(members__pk=request.user.pk)
        user_groups = Group.objects.filter(members__pk=request.user.pk)
        context = {
            'public_groups': public_groups,
            'user_groups': user_groups,
            'new_group_form': NewGroupForm()
        }
        return TemplateResponse(request, 'groups/list.html', context)


class GroupChat(View):

    form = NewPostForm

    @method_decorator(login_required)
    def get(self, request, group_id):
        """  Get all posts of a group and display them """
        group = Group.objects.get(pk=group_id)
        posts = Post.objects.filter(group=group).order_by('-time')
        context = {
            'posts': posts,
            'group': group,
            'post_form': self.form(),
        }
        return TemplateResponse(request, 'posts/list.html', context)

    @method_decorator(login_required)
    def post(self, request, group_id):
        """ Register a new post to a group """
        group = Group.objects.get(pk=group_id)
        post = Post(group=group, user=request.user)
        form = self.form(data=request.POST, instance=post)
        if form.is_valid():
            form.save()
            msg_level = messages.SUCCESS
            msg = _('Your post was saved successfully!')
        else:
            msg_level = messages.ERROR
            msg = _('Your post has some errors, check it out!')
        messages.add_message(request, msg_level, msg)
        return HttpResponseRedirect(reverse(
            'group_chat',
            kwargs={'group_id': group_id}
        ))


class GroupView(View):

    form = NewGroupForm

    @method_decorator(login_required)
    def post(self, request):
        group = Group(owner=request.user)
        form = self.form(data=request.POST, instance=group)
        if form.is_valid():
            form.save()
            msg_level = messages.SUCCESS
            msg = _('Your group was created!')
        else:
            msg_level = messages.ERROR
            msg = _('Couldn\'t create this group, check it out!')
        messages.add_message(request, msg_level, msg)
        return HttpResponseRedirect(reverse('list_groups'))

@login_required
def delete_post(request, post_id):
    """ Delete a group post if the owner is the current user """
    post = Post.objects.get(pk=post_id)
    if(post.user == request.user):
        post.delete()
        msg_level = messages.SUCCESS
        msg = _('Post deleted with success!')
    else:
        msg_level = messages.ERROR
        msg = _('You cannot delete somebody else\'s post!')
    messages.add_message(request, msg_level, msg)
    return HttpResponseRedirect(reverse(
        'group_chat',
        kwargs={'group_id': post.group.pk}
    ))


@login_required
def join_group(request, group_id):
    """ Enrolls the current user to a given group """
    group = Group.objects.get(pk=group_id)
    user_group, created = UserGroup.objects.get_or_create(
        user=request.user,
        group=group
    )
    msg_level = messages.SUCCESS if created else messages.WARNING
    msg = _('Congrats! You have joined the group %s.' % group.name)\
        if created \
        else _('You are already in group %s.' % group.name)
    messages.add_message(request, msg_level, msg)
    return HttpResponseRedirect(reverse(
        'group_chat',
        kwargs={'group_id': group_id}
    ))
