import os
from celery import Celery
from celery.schedules import crontab

#Второй строчкой мы связываем настройки Django с настройками Celery через переменную окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'News_Portal.settings')

#Далее мы создаём экземпляр приложения Celery и устанавливаем для него файл конфигурации(указать название ПРОЕКТА)
app = Celery('News_Portal')
#Мы также указываем пространство имён, чтобы Celery сам находил все необходимые настройки
# в общем конфигурационном файле settings.py. Он их будет искать по шаблону «CELERY_***»
app.config_from_object('django.conf:settings', namespace='CELERY')

#Последней строчкой мы указываем Celery автоматически искать задания в файлах tasks.py каждого приложения проекта
app.autodiscover_tasks()

#РАСПИСАНИЕ, по которому должны будут запускаться задачи. Само расписание
# представляет собой словарь словарей. Ключ основного словаря — это имя периодической задачи. Значение — это словарь
# с параметрами периодической задачи — сама задача, которая будет выполняться, аргументы, а также параметры расписания.
app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'news_p.tasks.weekly_send_mail',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': '',
    },
}