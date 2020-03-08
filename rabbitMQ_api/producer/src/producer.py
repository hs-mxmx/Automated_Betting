import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='consumers')
while True:
    channel.basic_publish(exchange='',
                        routing_key='consumers', 
                        body='hello World!')
    print('Message sent.')
    time.sleep(2)
    
connection.close()