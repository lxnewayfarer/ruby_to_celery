import pika
from celery import Celery
from tasks import send_response

app = Celery('app', broker='pyamqp://guest:guest@localhost//', result_backend='rpc://')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='responses')

channel.queue_declare(queue='requests')



def callback(ch, method, properties, body):
    send_response.apply_async(args=[body.decode(), properties.correlation_id])
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='requests', on_message_callback=callback)

channel.start_consuming()
