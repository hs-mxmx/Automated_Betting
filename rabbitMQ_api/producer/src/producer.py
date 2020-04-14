import pika
import time
import os
import myClients
import random
from dotenv import load_dotenv
from pathlib import Path


class Producer:

    def init(self):
        self.exchange = ''
        self.queue = ''
        self.amqp_url = ''
        self.routing_key = ''


    def producer(self):
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        self.exchange=os.getenv("EXCHANGE")
        self.queue=os.getenv("QUEUE")
        self.amqp_url=os.getenv("AMQP_URL")
        self.routing_key=os.getenv("ROUTING_KEY")
        print('URL: %s' % (self.amqp_url))

        parameters = pika.URLParameters(self.amqp_url)
        parameters.socket_timeout = 5
        connection = pika.BlockingConnection(parameters) # Connect to CloudAMQP
        try:
            self.opened_connection(connection) 

        except KeyboardInterrupt:
            print("[-] Quitting pruducer ...")
            connection.close()


    def opened_connection(self, connection):
        print("[!] Starting channel...")
        channel = connection.channel()
        self.send_message(channel)


    def send_message(self, channel):
        MAX_CLIENTS = 5
        myClient = myClients.myClients(random.randint(0,MAX_CLIENTS),'','','')
        myClient.createClient()
        msg = "{}_{}_{}_({})".format(myClient.id, myClient.company, myClient.price, myClient.date)
        channel.basic_publish(exchange='', routing_key=self.queue, body=msg)
        print("[*] Message published: {} ".format(msg))
        time.sleep(2)
        self.send_message(channel)



if __name__ == '__main__':
    my_producer = Producer()
    my_producer.producer()