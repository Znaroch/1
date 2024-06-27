import datetime

from celery import shared_task
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from .models import Post, Category

@shared_task
def send_mails_subscribers_new_post(pk):
    #по id(pk) создаваемого поста получаю сам пост
    post = Post.objects.get(pk=pk)
    #получаю категории поста
    categories = post.category.all()
    # Список подписчиков его передать в функцию для рассылки
    subscribers_list = []

    #в цикле получаю подписчиков этих категорий
    for cat in categories:
        subscribers = cat.subscribers.all()
        subscribers_list += [s for s in subscribers]

    for s in subscribers_list:
        #получаю имя подписчика
        sub_name = s.username
        #получаю почту подписчика, она должна быть списком или словарем, что бы работало
        sub_email = [s.email]
        html_content = render_to_string(
            'post_created_email.html',
            {
                'text': post.preview(),
                'link': f'{settings.SITE_URL}/news/{pk}',
                'sub_name': sub_name

            }
        )

        msg = EmailMultiAlternatives(
            subject=post.title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=sub_email,
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

@shared_task
def weekly_send_mail():
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

