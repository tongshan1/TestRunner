# -*- coding: utf-8 -*-
from kombu import Exchange, Queue
from celery import Celery

_celery = None


def init_celery(config):
    global _celery
    version, broker, backend = config['SERVICE_VERSION'], config['CELERY_BROKER_URL'], config['CELERY_RESULT_BACKEND']
    celery = Celery('TestRunner-{}'.format(version))
    _celery = celery
    celery.conf.update(

        CELERY_QUEUES=(
            Queue('cases', Exchange('interface_case'), routing_key="default"),

        ),
        CELERY_DEFAULT_QUEUE='celery',
        CELERY_DEFAULT_ROUTING_KEY='default',
        CELERY_DEFAULT_EXCHANGE_TYPE='direct',

        BROKER_URL=broker,
        CELERY_RESULT_BACKEND=backend,
        CELERY_RESULT_PERSISTENT=False,
        CELERY_TASK_RESULT_EXPIRES=300,
        CELERY_TASK_SERIALIZER='json',
        CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
        CELERY_RESULT_SERIALIZER='json',
        CELERY_TIMEZONE='Asia/Shanghai',
        CELERY_ENABLE_UTC=True,
        TOTORO_AMQP_CONNECTION_POOL={
            'max_idle_connections': 1,
            'max_open_connections': 500,
            'max_recycle_sec': 3600
        },
    )