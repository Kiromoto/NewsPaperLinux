from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory, CategorySubscriber


def nullfy_postrating(modeladmin, request, queryset):
    queryset.update(post_rating=0)


def nullfy_commentrating(modeladmin, request, queryset):
    queryset.update(comment_rating=0)


nullfy_commentrating.short_description = 'Обнулить рейтинг комментария'


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_title', 'post_text', 'get_category', 'post_rating', 'post_create_datetime',)
    list_filter = ('author', 'post_title', 'post_rating', 'post_create_datetime',)
    search_fields = ('post_title', 'post_text',)
    actions = [nullfy_postrating]


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_user', 'author_rating',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_subscribers',)
    search_fields = ('id', 'name',)


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'category_id',)
    list_filter = ('category_id', )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('postComment', 'user', 'comment_text', 'comment_rating', 'comment_datetime',)
    search_fields = ('postComment', 'comment_test',)
    actions = [nullfy_commentrating]


class CategorySubscriberAdmin(admin.ModelAdmin):
    list_display = ('subscriber_user', 'category_name',)
    search_fields = ('subscriber_user', 'category_name',)
    search_filter = ('subscriber_user', 'category_name',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CategorySubscriber, CategorySubscriberAdmin)
