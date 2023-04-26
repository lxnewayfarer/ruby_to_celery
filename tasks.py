import pika
from celery import Celery
import time

app = Celery('tasks', broker='pyamqp://guest:guest@localhost//', result_backend='rpc://')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='responses')


@app.task
def send_response(request, correlation_id):
    # Heavy task
    time.sleep(5)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='responses')
    
    channel.basic_publish(exchange='',
                          routing_key='responses',
                          properties=pika.BasicProperties(correlation_id=correlation_id),
                          body=request[::-1])
