from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from .models import Category, PostCategory, User, CategorySubscriber
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail


@receiver(m2m_changed, sender=PostCategory)
def postcategory_create(sender, instance, action, **kwargs):

    # recipient_email_list = ['kiromotossindzi@gmail.com', ]
    recipient_email_list = []

    try:
        cat = PostCategory.objects.filter(post_id=instance.id).values('category_id')
        idcat = cat[0]["category_id"]
        namecat = Category.objects.filter(postcategory__post_id=instance.id)
        y1 = CategorySubscriber.objects.filter(category_name=idcat)
        if y1:
            for el in y1:
                u = User.objects.get(id=el.subscriber_user_id)
                if u.email and u.email not in recipient_email_list:
                    recipient_email_list.append(u.email)
    except Exception:
        print('Ошибка получения данных о категории')
    else:
        subject = f'Опубликована новая статья в вашей любимой категории "{namecat[0].name}" на NewsPaper.'
        ur = f'http://127.0.0.1:8000{instance.get_absolute_url()}'
        html_content = render_to_string('post_emailsend.html', {'post': instance, 'ur': ur, })
        msg = EmailMultiAlternatives(subject=subject,
                                     body=instance.post_text[:20],
                                     from_email='tlfordjango@mail.ru',
                                     to=recipient_email_list,
                                     )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()
    finally:
        print(f'Print from signals.py: {recipient_email_list}')

