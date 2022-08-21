from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        import news.signals

        # from .tasks import weekly_mails
        # from .scheduler import scheduler
        # print('def ready...OK! import...OK! Started from apps.py!')
        #
        # scheduler.add_job(
        #     id='mail send',
        #     func=weekly_mails,
        #     trigger='interval',
        #     seconds=20,
        #     # weeks=1,
        # )

        # scheduler.start()
