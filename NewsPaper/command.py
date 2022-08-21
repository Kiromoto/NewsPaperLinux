from news.models import *
from datetime import datetime, date, time

user1 = User.objects.create_user(username='UserFirst')
user2 = User.objects.create_user(username='UserSecond')
user3 = User.objects.create_user(username='UserThird')
user4 = User.objects.create_user(username='User4')

author1 = Author.objects.create(author_user=user1)
author2 = Author.objects.create(author_user=user2)
author3 = Author.objects.create(author_user=user3)
author4 = Author.objects.create(author_user=user4)

Category.objects.create(name='Экономика')
Category.objects.create(name='Наука')
Category.objects.create(name='Спорт')
Category.objects.create(name='Авто')

Post.objects.create(author=Author.objects.get(id=1), type_of_post=Post.ARTICLE, post_title='Статья первая',
                    post_text='Про тенденции 2021-2022 года в массовом производстве автомобилей')

Post.objects.create(author=Author.objects.get(id=1), type_of_post=Post.ARTICLE, post_title='Статья вторая',
                    post_text='Про необходимость развития материальной базы для подготовки спортсменов к олимпиаде')

Post.objects.create(author=Author.objects.get(id=1), type_of_post=Post.NEWS, post_title='Новость первая',
                    post_text='Солнечный свет связали с голодом у мужчин')

Post.objects.create(author=Author.objects.get(id=2), type_of_post=Post.NEWS, post_title='Новость вторая',
                    post_text='Новость про науку и спорт')

Post.objects.get(id=1).post_category.add(Category.objects.get(id=1))
Post.objects.get(id=1).post_category.add(Category.objects.get(id=4))
Post.objects.get(id=2).post_category.add(Category.objects.get(id=1))
Post.objects.get(id=2).post_category.add(Category.objects.get(id=3))
Post.objects.get(id=3).post_category.add(Category.objects.get(id=1))
Post.objects.get(id=3).post_category.add(Category.objects.get(id=2))
Post.objects.get(id=4).post_category.add(Category.objects.get(id=2))
Post.objects.get(id=4).post_category.add(Category.objects.get(id=3))



Comment.objects.create(postComment=Post.objects.get(id=1), user=User.objects.get(id=2), comment_text='com10_ok!')
Comment.objects.create(postComment=Post.objects.get(id=1), user=User.objects.get(id=3), comment_text='com11_ok!')
Comment.objects.create(postComment=Post.objects.get(id=2), user=User.objects.get(id=4), comment_text='com21_ok!')
Comment.objects.create(postComment=Post.objects.get(id=3), user=User.objects.get(id=2), comment_text='com31_ok!')
Comment.objects.create(postComment=Post.objects.get(id=4), user=User.objects.get(id=1), comment_text='com41_ok!')


Comment.objects.get(id=1).like()
Comment.objects.get(id=1).like()
Comment.objects.get(id=1).like()
Comment.objects.get(id=1).dislike()

Comment.objects.get(id=2).like()
Comment.objects.get(id=2).dislike()
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).dislike()
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).dislike()
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=2).dislike()

Comment.objects.get(id=3).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=3).dislike()

Comment.objects.get(id=4).dislike()
Comment.objects.get(id=4).dislike()
Comment.objects.get(id=4).dislike()
Comment.objects.get(id=4).like()
Comment.objects.get(id=4).like()
Comment.objects.get(id=4).like()
Comment.objects.get(id=4).like()
Comment.objects.get(id=4).like()
Comment.objects.get(id=4).like()

al = Author.objects.all()
for i in al:
    i.rating_update()
    i.author_rating

a = Author.objects.order_by('-author_rating')[:1]
for i in a:
    i.author_user.username
    i.author_rating

p = Post.objects.order_by('-post_rating')[:1]
for i in p:
    i.post_create_datetime
    i.author.author_user.username
    i.post_rating
    i.post_title
    i.preview()


for i in p:
    print(i.postComment)




# python manage.py shell
# from news.models import *
# a = Author.objects.all()
# for i in a:
#     i.author_user.username
#     i.update_rating()
#     i.author_rating
