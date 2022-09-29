from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, CategorySubscriber, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.core.cache import cache

from django.views import View
from django.http.response import HttpResponse
from django.utils.translation import gettext as _
from django.utils.translation import activate, get_supported_language_variant

from django.utils import timezone
import pytz

import logging

logger = logging.getLogger(__name__)

# class Index(View):
#     def get(self, request):
#         current_time = timezone.now()
#         print(current_time)
#         print(pytz.common_timezones)
#
#         context = {
#             'current_time': current_time,
#             'timezones': pytz.common_timezones,
#         }
#         return HttpResponse(render(request, 'default.html', context))
#
#     def post(self, request):
#         request.session['django_timezone'] = request.POST['timezone']
#         return redirect('news/')


class PostList(ListView):
    model = Post
    ordering = '-post_create_datetime'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get(self, request):
        current_time = timezone.now()
        print(current_time)
        print(timezone.get_current_timezone())
        news = Post.objects.all()

        context = {
            'current_time': current_time,
            'timezones': pytz.common_timezones,
            'news': news,
        }
        return HttpResponse(render(request, 'news.html', context))

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('http://127.0.0.1:8000/news/')



class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        print(Post.objects.get(pk=id).post_title)
        print(self.request.user.username, self.request.user.id)

        context['is_subscribe'] = False
    #     # print(Post.objects.get(id=id).post_title)
    #     qwe = Category.objects.filter(pk=Post.objects.get(pk=id).post_category.id).values('subscriber__username')
    #     print(qwe)
    #     context['is_not_subscribe'] = not qwe.filter(subscriber__username=self.request.user).exists()
    #     context['is_subscribe'] = qwe.filter(subscriber__username=self.request.user).exists()
        return context


# def add_subscribe(request, **kwargs):
#     pk = request.GET.get('pk',)
#     print('Пользователь', request.user, 'добавлен в подписчики:', Category.objects.get(pk=pk))
#     Category.objects.get(pk=pk).subscriber.add(request.user)
#     return redirect('/news/')

@login_required
def subscribe_me(request, pk):
    user = request.user
    print(f'{user} и его ID: {user.id}')
    print('Пользователю', user, 'добавлена в подписки категория:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscriber.add(user)
    category_for_this_user = CategorySubscriber.objects.filter(subscriber_user=user.id).values('category_name')
    for i in category_for_this_user:
        n = i['category_name']
        print(f'{n} - {Category.objects.get(pk=n)}')

    return redirect('/')

# @login_required
# def unsubscribe_me(request, **kwargs):
#     user = request.user
#     pk = kwargs.get('pk',)
#     print(f'kwargs.get("pk",)= {pk}')
#     print(f'{user} и его ID: {user.id}')
#         # print('Пользователь', user, 'отписан от категории:', Category.objects.get(pk=pk))
#         # Category.objects.get(pk=pk).subscriber.add(user)
#         # category_for_this_user = CategorySubscriber.objects.filter(subscriber_user=user.id).values('category_name')
#         # for i in category_for_this_user:
#         #     n = i['category_name']
#         #     print(f'{n} - {Category.objects.get(pk=n)}')
#
#     return redirect('/')

    # pk = request.GET.get('pk', )
    # print('Пользователю', request.user, 'добавлена категория в подписки:', Category.objects.get(pk=pk))

    # user = request.user
    # authors_group = Group.objects.get(name='authors')
    # if not request.user.groups.filter(name='authors').exists():
    #     authors_group.user_set.add(user)


# @login_required
# def upgrade_me(request):
#     user = request.user
#     authors_group = Group.objects.get(name='authors')
#     if not request.user.groups.filter(name='authors').exists():
#         authors_group.user_set.add(user)
#     return redirect('/news/')


class PostSearch(ListView):
    model = Post
    ordering = '-post_create_datetime'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')

