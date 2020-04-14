import pika
import time
import os
import queue
from flask import Flask
from flask import render_template
from datetime import datetime
from threading import Thread
import dbBalancer
import logging
from dotenv import load_dotenv
from pathlib import Path
import informer
import flask_server 

# Docker Log Route
# LOG_ROUTE = os.path.dirname(__file__) + '/logs/'

""" TROUBLESHOOTING """
# Windows alternative Route
LOG_ROUTE = os.path.abspath(os.curdir) + '/logs/'

# Only for Docker Image (Linux)
# LOG_ROUTE = os.path.dirname(os.path.relpath(__file__)) + '/logs/'

class Consumer:

    def init(self):
        self.exchange = ''
        self.queue = ''
        self.amqp_url = ''
        self.table = ''
        self.backup = ''
        self.informer = ''


    def main(self):
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        self.exchange=os.getenv("EXCHANGE")
        self.queue=os.getenv("QUEUE")
        self.amqp_url=os.getenv("AMQP_URL")
        self.table=os.getenv("MYTABLE")
        self.backup=os.getenv("BACKUP_ROUTE")
        self.informer = informer.Informer()

        parameters = pika.URLParameters(self.amqp_url)
        connection = pika.BlockingConnection(parameters) # Connect to CloudAMQP
        try:
            self.opened_connection(connection) 

        except KeyboardInterrupt:
            print("[-] Quitting consumer ...")
            connection.close()


    def opened_connection(self, connection):
        """Connection stablished"""
        channel = connection.channel()
        self.opened_qos(channel,connection)


    def opened_qos(self, channel, connection):
        """QoS Queue"""
        channel.basic_qos(prefetch_count=1, 
        callback=self.opened_queue(channel,connection))


    def opened_queue(self, channel, connection):
        """Opened Queue"""
        channel.queue_bind(queue=self.queue, exchange= '', routing_key=self.queue, callback=self.open_message(channel, connection))


    def callback(self, ch, method, properties, body):
        self.read_message(body)


    def open_message(self, channel, connection):
        channel.basic_consume(queue=self.queue, on_message_callback=self.callback, auto_ack=True)
        print("Waiting for messages...")
        thread = Thread(channel.start_consuming())
        thread.start()


    def read_message(self, msg):
        msg = msg.decode("utf-8")
        self.saveFile(msg)
        print("Message: %r " % msg)
        time.sleep(1)
        return


    def saveFile(self, msg):
        DATE = datetime.now()
        LOG_FILE = DATE.strftime('%b_%d_%Y') + ".txt"
        LOG_TEMP = "temp-"+ LOG_FILE
        temp_msg = msg
        msg = "[" + str(datetime.time(datetime.now())) + "]: " + msg
        try:
            file = open(LOG_ROUTE + LOG_FILE, "a")
            file.write("\n" + msg)
            file.close()
            file_temp = open(LOG_ROUTE + LOG_TEMP, "a")
            file_temp.write("\n" + temp_msg)
            file.close()
            # Database Import
            myDatabase = dbBalancer.dbConnection()
            threadSave = Thread(target=myDatabase.enableConnection(temp_msg))
            threadSave.start()
            # threadData = Thread(target=myDatabase.getData(MYTABLE))
            # threadData.start()
            if(str(datetime.now().hour)+':'+str(datetime.now().minute)=='12:40'):
                if(int(datetime.now().second)>=0 and int(datetime.now().second)<=59):
                    Thread(target=self.informer.main()).start()

        except IOError:
            file = open(LOG_ROUTE + LOG_FILE, "w+")
            file.write("\n" + msg)
            file.close()
            file_temp = open(LOG_ROUTE + LOG_TEMP, "w+")
            file_temp.write("\n" + temp_msg)
            file_temp.close()
        
        

if __name__ == '__main__':
    my_consumer = Consumer()
    thread_consumer = Thread(target=my_consumer.main)
    thread_consumer.daemon = True
    thread_consumer.start()
    thread_flask = Thread(target=flask_server.main())



# def read_tempFile(logfile):
#     my_temp_list = []
#     with open(logfile, "r")as my_file: data = my_file.read().replace('\n', ' ')
#     my_temp_list = list(data.split(' '))
#     return my_temp_list