import pika
import time
import os

# RabbitMQ exchange
# EXCHANGE = 'my_exchange'

# AMQP routing key when sending a message
ROUTING_KEY = 'consumers_queue'

# AMQP queue
QUEUE = 'my_queue'

# Delay between messages
DELAY = 0.1

def main():
    # Location of ARabbitMQ server from AMQP_URL variable
    amqp_url = os.environ['AMQP_URL']
    print('URL: %s' % (amqp_url))

    # Stablish connection
    parameters = pika.URLParameters(amqp_url)
    parameters.socket_timeout = 5
    connection = pika.BlockingConnection(parameters) # Connect to CloudAMQP
    try:
        opened_connection(connection) 

    except KeyboardInterrupt:
        print("[-] Quitting pruducer ...")
        connection.close()


def opened_connection(connection):
    # Connection stablished
    print("[!] Starting channel...")
    channel = connection.channel()
    send_message(channel, 0)


def send_message(channel, i):
    msg = 'Message %d' % (i)
    channel.basic_publish(exchange='', routing_key=QUEUE, body=msg)
    print("[*] Message published: {} ".format(msg))
    time.sleep(2)
    send_message(channel, i+1)


if __name__ == '__main__':
    main()