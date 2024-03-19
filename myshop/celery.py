import os
from celery import Celery

# задаю стандартный модуль настроек Django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
# broker = "amqp://admin:111@http:5672/"
app = Celery('myshop', broker='amqp://guest:guest@172.25.224.1:5672//')#создается экземпляр приложения
app.config_from_object('django.conf:settings', namespace='CELERY')#загружается любая конкретно прикладная конфигурация из настроек проекта
app.autodiscover_tasks()



# docker pull rabbitmq      получить образ брокера сообщений RabbitMQ
#docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management запуск брокера RabbitMQ
# celery -A myshop worker -l info    Запуск Celery