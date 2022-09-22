from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy


class Author(models.Model):
    author_user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        verbose_name=pgettext_lazy('Author name', 'Author name'),
        help_text=_('Author name')
    )
    author_rating = models.IntegerField(
        default=0,
        verbose_name=pgettext_lazy('Author rating', 'Author rating'),
        help_text=_('Author rating')
    )

    def update_rating(self):
        # суммарный рейтинг каждой статьи автора умножается на 3;
        # !!! если у автора нет постов, то выдает ошибку. Нужно проверить.
        sum_post_rating = self.post_set.aggregate(allPostRating=models.Sum('post_rating'))
        postR = 0
        postR += sum_post_rating.get('allPostRating')

        # суммарный рейтинг всех комментариев автора;
        sum_comment_rating = self.author_user.comment_set.aggregate(authorCommentRating=models.Sum('comment_rating'))
        commR = 0
        commR += sum_comment_rating.get('authorCommentRating')

        # # # суммарный рейтинг всех комментариев к статьям автора.
        # sum_PostComment_rating = self.author_user.post.postComment_set.aggregate(allCommentPostRating=models.Sum('comment_rating'))
        # pcommR = 0
        # pcommR += sum_PostComment_rating.get('allCommentPostRating')

        self.author_rating = postR * 3 + commR  # + pcommR
        self.save()

    def __str__(self):
        return self.author_user.username


class Category(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name=pgettext_lazy('Name of category', 'Name of category'),
        help_text=_('category name')
    )
    subscriber = models.ManyToManyField(
        User, through='CategorySubscriber',
        blank=True,
        verbose_name=pgettext_lazy('Subscribers', 'Subscribers'),
        help_text=_('subscribers')
    )

    def get_subscribers(self):
        return ';\n'.join([s.username for s in self.subscriber.all()])

    def __str__(self):
        return self.name


class CategorySubscriber(models.Model):
    subscriber_user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        blank=True, null=True,
        help_text=_('subscriber')
    )
    category_name = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text=_('category name')
    )


class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AT'

    CHOISE_NW_AT = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    ]

    author = models.ForeignKey(
        Author, on_delete=models.CASCADE,
        verbose_name=pgettext_lazy('Author name', 'Author name'),
        help_text=_('Author name')
    )
    type_of_post = models.CharField(
        max_length=2,
        default=NEWS,
        choices=CHOISE_NW_AT,
        verbose_name=pgettext_lazy('Post type', 'Post type'),
        help_text=_('Post type')
    )
    post_create_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name=pgettext_lazy('Time and date of publication', 'Time and date of publication'),
        help_text=_('Time and date of publication')
    )
    post_category = models.ManyToManyField(
        Category, through='PostCategory',
        related_name='posts',
        verbose_name=pgettext_lazy('This is category of post', 'Post category'),
        help_text=_('Post category')
    )
    post_title = models.CharField(
        max_length=128,
        verbose_name=pgettext_lazy('Post title', 'Post title'),
        help_text=_('Post title')
    )
    post_text = models.TextField(
        verbose_name=pgettext_lazy('The content of the post', 'The content of the post'),
        help_text=_('The content of the post')
    )
    post_rating = models.IntegerField(
        default=0,
        verbose_name=pgettext_lazy('The rating of the post', 'The rating of the post'),
        help_text=_('The rating of the post')
    )
    is_updated = models.BooleanField(
        default=False
    )
    is_new = models.BooleanField(
        default=True,
        help_text=_('Is this article new?')
    )

    def get_category(self):
        return '\n'.join([c.name for c in self.post_category.all()])

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.post_text[:124]}...'

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse('new_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        help_text=_('The rating of the post')
    )
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    postComment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_datetime = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
