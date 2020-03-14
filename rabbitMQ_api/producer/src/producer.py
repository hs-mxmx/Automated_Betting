import pika
import time
import os
import myClients
import random


# RabbitMQ exchange
# EXCHANGE = 'my_exchange'

# AMQP routing key when sending a message
ROUTING_KEY = 'consumers_queue'

# AMQP queue
QUEUE = 'my_queue'

# Delay between messages
DELAY = 0.1

# Number of clients
MAX_CLIENTS = 5

def main():
    # Location of ARabbitMQ server from AMQP_URL variable
    amqp_url = "amqp://xxalaqou:dQFGDDlp-pfhSolv57XHhVWeqmzcmD6l@crow.rmq.cloudamqp.com/xxalaqou"
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
    myClient = myClients.myClients(random.randint(0,MAX_CLIENTS),'','','')
    myClient.createClient()
    msg = "{}_{}_{}_({})".format(myClient.id, myClient.company, myClient.price, myClient.date)
    channel.basic_publish(exchange='', routing_key=QUEUE, body=msg)
    print("[*] Message published: {} ".format(msg))
    time.sleep(2)
    send_message(channel, i+1)

#    print("{}_{}_{}({})".format(myClient.id, myClient.company, myClient.price, myClient.date))


if __name__ == '__main__':
    main()