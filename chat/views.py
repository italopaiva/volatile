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
        pass