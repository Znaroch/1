'''
Закоментировал, что бы рассылка работала через Redis и Celery
import logging
import datetime

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news_p.models import Post, Category

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    #все посты дата создания, которыъ равна или больше даты недельной давности
    posts = Post.objects.filter(date__gte=last_week)
    #список значений(названия категорий) категорий постов,
    # flat=True что бы получить список строк, а не кортежей со строками внутри
    #set - множество, что бы имена категорий не повторялись
    categories = set(posts.values_list('category__name', flat=True))
    #список подписчиков, через модель Category фильтрую по названию категорий из categories
    #через values_list обращаюсь к подписчикам категорий и получаю их email и имена пользователей
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', 'subscribers__username'))
    #в subscribers получаю множество из кортежей на первом месте email на втором username
    #далее в цикле в переменные с именем и почтой по индексам из кортежей получаю данные для передачи
    #в html_content и msg
    for s in subscribers:
        sub_name = s[1]
        sub_email = [s[0]]
        html_content = render_to_string(
            'weekly_posts.html',
            {
                'link': settings.SITE_URL,
                'posts': posts,
                'sub_name': sub_name
            }
        )

        msg = EmailMultiAlternatives(
            subject='Недельная рассылка сообщений',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=sub_email,
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="wed", hour="14", minute="31"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
'''