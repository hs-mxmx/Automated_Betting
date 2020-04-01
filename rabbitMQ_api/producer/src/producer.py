import pika
import time
import os
import myClients
import random
from dotenv import load_dotenv
from pathlib import Path

# readEnv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
EXCHANGE=os.getenv("EXCHANGE")
QUEUE=os.getenv("QUEUE")
AMQP_URL=os.getenv("AMQP_URL")
ROUTING_KEY=os.getenv("ROUTING_KEY")

# Delay between messages
DELAY = 0.1

# Number of clients
MAX_CLIENTS = 5

def main():
    # Location of ARabbitMQ server from AMQP_URL variable
    print('URL: %s' % (AMQP_URL))

    # Stablish connection
    parameters = pika.URLParameters(AMQP_URL)
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