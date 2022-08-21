from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# ______________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________
# Код итогового задания
class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

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
    name = models.CharField(max_length=64, unique=True)
    subscriber = models.ManyToManyField(User, through='CategorySubscriber', blank=True)

    def __str__(self):
        return self.name

class CategorySubscriber(models.Model):
    subscriber_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AT'

    CHOISE_NW_AT = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_of_post = models.CharField(max_length=2, default=NEWS, choices=CHOISE_NW_AT)
    post_create_datetime = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory', related_name='posts')
    post_title = models.CharField(max_length=128)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)
    is_updated = models.BooleanField(default=False)

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
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
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
