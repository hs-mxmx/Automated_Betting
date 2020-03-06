import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='consumers')
channel.basic_publish(exchange='',
                      routing_key='consumers', 
                      body='hello World!')
print('Message sent.')
connection.close()