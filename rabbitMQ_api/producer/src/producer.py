import pika
import time
import os
import provider_data as pv
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
        self.exchange='my_exchange'
        self.queue='my_queue'
        self.amqp_url='amqp://xxalaqou:dQFGDDlp-pfhSolv57XHhVWeqmzcmD6l@crow.rmq.cloudamqp.com/xxalaqou'
        self.routing_key = self.queue
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
        channel.queue_declare(queue=self.queue, durable=True)
        self.send_message(channel)

    
    def send_message(self, channel):
        provider = pv.Provider()
        msg, content = provider.generate_provider()
        channel.basic_publish(exchange='', routing_key=self.routing_key, body=str(content))
        print("[*] Message published: {} ".format(msg))
        time.sleep(2)
        self.send_message(channel)


if __name__ == '__main__':
    my_producer = Producer()
    my_producer.producer()
