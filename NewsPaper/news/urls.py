from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostCreate, PostEdit, PostDelete, subscribe_me, unsubscribe_me

from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60*1)(PostList.as_view()), name='news_list'),
    path('<int:pk>', cache_page(60*5) (PostDetail.as_view()), name='new_detail'),
    path('search/', PostSearch.as_view(), name='news_search'),
    path('create/', PostCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='new_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='new_delete'),
    path('search/?post_category=<int:pk>', PostSearch.as_view(), name='category_search'),
    path('subscribes/<int:pk>/', subscribe_me, name='subscr_me'),
    path('subscribes/<int:pk>/', unsubscribe_me, name='unsubscr_me'),



]
