from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from .models import BaseRegisterForm
from .forms import UserForm
from django.contrib.auth.mixins import LoginRequiredMixin


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    template_name = 'index.html'
    success_url = '/about/'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news/')


class UserEdit(LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = UserForm
    model = User
    template_name = 'user_edit.html'
    success_url = '/'
