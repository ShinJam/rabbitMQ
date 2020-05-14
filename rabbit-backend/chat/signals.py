from json import dumps

import django.dispatch
import pika
from django.dispatch import receiver

from config.settings import AMQP_URL

# 커스텀 시그널 정의
broadcast_published = django.dispatch.Signal(providing_args=(
    'source', 'source_display_name', 'obj', 'short_description', 'extra_data',
))


def connect():
    """RabbitMQ 커넥션"""
    params = pika.URLParameters(AMQP_URL)
    connection = pika.BlockingConnection(params)

    channel = connection.channel()

    return connection, channel


@receiver(broadcast_published)
def publish_broadcast(**kwargs):
    """RabbitMQ 큐에 메세지 삽입"""
    connection, channel = connect()

    uri = kwargs['extra_data']['uri']
    message = kwargs['extra_data']['message']

    channel.exchange_declare(exchange=uri, exchange_type='fanout')
    channel.basic_publish(exchange=uri, routing_key='', body=dumps(message))

    connection.close()
