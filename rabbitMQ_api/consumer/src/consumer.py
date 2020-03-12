import pika
import time
import os
from datetime import datetime


# RabbitMQ exchange
EXCHANGE = 'my_exchange'

# Name of rabbitMQ queue
QUEUE = 'my_queue'

# Log file
LOG_FILE = str(datetime.date(datetime.now())) + ".txt"

def main():
    # Location of ARabbitMQ server from AMQP_URL variable
    amqp_url = os.environ['AMQP_URL']
    print('URL: %s' % (amqp_url))

    # Stablish connection
    parameters = pika.URLParameters(amqp_url)
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
    opened_qos(channel,connection)


def opened_qos(channel, connection):
    print("[+] Queue QoS...")
    channel.basic_qos(prefetch_count=1, 
    callback=opened_queue(channel,connection))

def opened_queue(channel, connection):
    print("[+] Queue opened...")
    channel.queue_bind(queue=QUEUE, exchange= '', routing_key=QUEUE, callback=open_message(channel, connection))

def callback(ch, method, properties, body):
    print("Callback")
    read_message(body)

def open_message(channel, connection):
    print("Opening messages...")
    channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)
    print("Waiting for messages...")
    channel.start_consuming()


def read_message(msg):
    print("[+] Reading messages: \n")
    msg = msg.decode("utf-8")
    print("Message: %r " % msg)
    saveFile(LOG_FILE, msg)
    time.sleep(1)
    return


def saveFile(logfile, msg):
    msg = "[" + str(datetime.time(datetime.now())) + "]: " + msg
    try:
        my_dir = os.path.dirname(os.path.relpath(__file__))
        file = open(my_dir + "/" + logfile, "a")
        file.write("\n" + msg)
        file.close()
    except IOError:
        file = open(logfile, "w")
        file.write("\n" + msg)
        file.close()


if __name__ == '__main__':
    main()