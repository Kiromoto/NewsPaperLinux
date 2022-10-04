from datetime import datetime
import zoneinfo
#
# import pytz
#
from django.conf import settings
# from django.db.models import Count
# from django.db.models.functions import ExtractYear, ExtractMonth
from django.utils import timezone
import pytz

from .models import Category, Post


def navigate_context(request):
    current_time = timezone.datetime.now().astimezone()  # + timezone.timedelta(hours=3)
    print(f'Текущее время текущей таймзоны из context_processors.py: {current_time}')
    news = Post.objects.all()

    context = {
        'current_time': current_time,
        'timezones': pytz.common_timezones,
        'news': news,
    }
    #
    return context

#     """Контекст для блоков повторяющихся на всех страницах"""
#     category = Category.objects.all()
#     archives = Post.objects.annotate(
#         year=ExtractYear('date_pub'),
#         month=ExtractMonth('date_pub')
#     ).values('year', 'month').annotate(total=Count('id'))
#     user_timezone = pytz.timezone(
#         request.session.get('django_timezone') or settings.TIME_ZONE
#     )
#     current_time = timezone.now().astimezone(user_timezone)
#
#     context = {
#         'category': category,
#         'archives': archives,
#         'current_time': current_time,
#         'timezones': pytz.common_timezones,
#     }
#
#     return context
