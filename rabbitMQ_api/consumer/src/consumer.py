import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='consumers')

def callback(ch, method, properties, body):
    print(" Message received: %r" % body)

channel.basic_consume(queue='consumers',
                      auto_ack=True,
                      on_message_callback=callback)


print(' Waiting for message...')
channel.start_consuming()