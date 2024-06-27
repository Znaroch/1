from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .tasks import send_mails_subscribers_new_post
from .models import PostCategory



'''
Это для работы рассылки через сигналы
def send_notifications(preview, pk, title, subscribers_list):
#из списка подписчиков при каждой итерации цила отправляется сообщение 1 подписчику с обращением
#к конкретному подписчику в письме
    for s in subscribers_list:
        #получаю имя подписчика
        sub_name = s.username
        #получаю почту подписчика, она должна быть списком или словарем, что бы работало
        sub_email = [s.email]
        html_content = render_to_string(
            'post_created_email.html',
            {
                'text': preview,
                'link': f'{settings.SITE_URL}/news/{pk}',
                'sub_name': sub_name

            }
        )

        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=sub_email,
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
'''

@receiver(m2m_changed, sender=PostCategory)

def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        #вызов таски рассылки при создании поста
        send_mails_subscribers_new_post.delay(instance.pk)
        '''
        Это для работы рассылки через сигналы
        categories = instance.category.all()
        #Список подписчиков его передать в функцию для рассылки
        subscribers_list = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_list += [s for s in subscribers]
            
        send_notifications(instance.preview, instance.pk, instance.title, subscribers_list)
        '''
