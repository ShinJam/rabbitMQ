import sys

import pika
import uwsgi

from config.settings import AMQP_URL


def application(env, start_response):
    """웹소켓 서버 세팅, 메세지큐 consume"""
    params = pika.URLParameters(AMQP_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    exchange = env['PATH_INFO'].replace('/', '')

    channel.exchange_declare(
        exchange=exchange, exchange_type='fanout'
    )

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=exchange, queue=queue_name)

    uwsgi.websocket_handshake(
        env['HTTP_SEC_WEBSOCKET_KEY'],
        env.get('HTTP_ORIGIN', '')
    )

    def keepalive():
        """Keep the websocket connection alive (called every 30 seconds)."""
        print('PING/PONG...')
        try:
            uwsgi.websocket_recv_nb()
            connection.call_later(30, keepalive)
        except OSError as error:
            print(error)
            sys.exit(1)  # Kill process and force uWSGI to Respawn

    keepalive()

    while True:
        for method_frame, _, body in channel.consume(queue_name):
            try:
                uwsgi.websocket_send(body)
            except OSError as error:
                print(error)
                sys.exit(1)  # Force uWSGI to Respawn
            else:
                # acknowledge the message
                channel.basic_ack(method_frame.delivery_tag)
