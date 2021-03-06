import pika
import time
import os
import queue
from datetime import datetime
from threading import Thread
import dbBalancer
import logging
from dotenv import load_dotenv
from pathlib import Path
import informer
import flask_server 
import json
import utils.consumer_mapping as cm
import ast

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
        self.routing_key = ''
        self.queue = ''
        self.amqp_url = ''
        self.table = ''
        self.backup = ''
        self.info_check = ''


    def opened_connection(self, connection):
        # @param connection Pika.Blocking.Object
        """Connection stablished"""
        channel = connection.channel()
        self.opened_qos(channel,connection)


    def opened_qos(self, channel, connection):
        # @param connection Pika.Blocking.Object
        # @param channel Pika.Blocking.Channel
        """QoS Queue"""
        channel.queue_declare(queue=self.queue, durable=True)
        channel.basic_qos(prefetch_count=1, 
        callback=self.opened_queue(channel,connection))


    def opened_queue(self, channel, connection):
        # @param connection Pika.Blocking.Object
        # @param channel Pika.Blocking.Channel
        """Opened Queue"""
        channel.queue_bind(queue=self.queue, exchange= '', routing_key=self.routing_key, callback=self.open_message(channel, connection))


    def callback(self, ch, method, properties, body):
        # @param method Pika.Basic.Deliver
        # @param properties Pika.BasicProperties
        # @param body Bytes
        self.read_message(body)


    def open_message(self, channel, connection):
        # @param connection Pika.Blocking.Object
        # @param channel Pika.Blocking.Channel
        """Connected to Queue"""
        channel.basic_consume(queue=self.queue, on_message_callback=self.callback, auto_ack=True)
        print("Waiting for messages...")
        thread = Thread(channel.start_consuming())
        thread.start()


    def read_message(self, msg):
        # @param msg Bytes
        """Read messages from queue"""
        msg = msg.decode(cm.UTF)
        self.saveFile(msg)
        time.sleep(1)
        return


    def saveFile(self, msg):
        # @param msg String
        """Save file and create informer"""
        DATE = datetime.now()
        LOG_FILE = DATE.strftime(cm.DATE_FORMAT) + cm.TXT
        LOG_TEMP = cm.TEMP + LOG_FILE
        temp_msg = msg
        msg = "[" + str(datetime.time(datetime.now())) + "]: " + msg
        try:
            file = open(LOG_ROUTE + LOG_FILE, "a")
            file.write("\n" + msg)
            file.close()
            file_temp = open(LOG_ROUTE + LOG_TEMP, "a")
            file_temp.write("\n" + temp_msg)
            file.close()
            self.generate_file(temp_msg)
            if(str(datetime.now().hour)+':'+str(datetime.now().minute) == cm.INFORMER_TIMER):
                if (int(datetime.now().second) >= cm.INFORMER_MIN_TIME 
                or int(datetime.now().second) <= cm.INFORMER_MAX_TIME
                and self.info_check == False):
                    self.info_check = True
                    my_informer = informer.Informer()
                    Thread(target=my_informer.main(self.info_check)).start()

        except IOError:
            print(LOG_ROUTE)
            if not os.path.isdir(LOG_ROUTE):
                os.makedirs(LOG_ROUTE)
            file = open(LOG_ROUTE + LOG_FILE, "w+")
            file.write("\n" + msg)
            file.close()
            file_temp = open(LOG_ROUTE + LOG_TEMP, "w+")
            file_temp.write("\n" + temp_msg)
            file_temp.close()
        
 
    def generate_file(self, provider_data):
        # @param provider_data String
        """Convert provider_data to dict and map to storage"""
        current_dir = os.path.dirname(os.path.realpath(__file__))
        provider_data = ast.literal_eval(provider_data)
        name, date = self.extract_metadata(provider_data)
        file = (name + cm.SEPARATOR + date + cm.FILE_START + cm.JSON)
        path = (current_dir + cm.CATALOGUES_ROUTE + name + '/')
        file = self.check_file(path, file)
        try:
            if not os.path.isdir(path):
                os.makedirs(path)
            with open(path + file, 'a') as jsonfile:
                json.dump(provider_data, jsonfile, indent=4, separators=(',', ': '), sort_keys=True)
            # self.check_file(file)
        except Exception as ex:
            print(ex)

        
    def check_file(self, path, file):
        # @param path String
        # @param file String
        """Check if specified file exists in path, otherwise create it"""
        try:
            if os.path.exists(path + file):
                file = file.split(cm.SEPARATOR)
                id = file[2].split('.')
                new_id = cm.SEPARATOR + str(int(id[0]) + 1)
                new_file = (file[0] + cm.SEPARATOR + file[1] + new_id + cm.JSON)
                while os.path.exists(path + new_file):
                    new_file = self.check_file(path, new_file)
                return new_file
            return file
        except Exception as ex:
            print(ex)
            pass

    
    def extract_metadata(self, content):
        # @param content dictionary
        """Extract data from provider dictionary"""
        info_resume = []
        for provider in content:
            for items in content[provider][cm.METADATA]:
                contentType = items[cm.CONTENTYPE]
                content = items[cm.CONTENT]
                country = items[cm.COUNTRY]
                final_date = items[cm.DATE]
                price = int(items[cm.PRICE])
                date = [final_date.split(cm.SEPARATOR)]
                date = date[0]
                date = datetime.strptime(date[0], cm.DATE_FORMAT)
                info_resume = [provider, date, contentType, content, country, price]
                self.databaseImport(info_resume, provider)


        return provider, str(final_date)
              
    
    def databaseImport(self, info, provider):
        # @param info Array
        # @param provider String
        # Database Import
        myDatabase = dbBalancer.dbConnection()
        threadSave = Thread(target=myDatabase.enableConnection(info, provider))
        threadSave.start()

    
    def setEnv(self):
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        self.exchange=os.getenv("EXCHANGE")
        self.queue=os.getenv("QUEUE")
        self.routing_key=self.queue
        self.amqp_url=os.getenv("AMQP_URL")
        self.table=os.getenv("MYTABLE")
        self.backup=os.getenv("BACKUP_ROUTE")


    def main(self):
        self.setEnv()
        self.informer = informer.Informer()
        self.info_check = False

        parameters = pika.URLParameters(self.amqp_url)
        connection = pika.BlockingConnection(parameters) # Connect to CloudAMQP
        try:
            print("Stablishing connection...")
            self.opened_connection(connection) 

        except Exception as ex:
            print("[-] Quitting consumer ...")
            print(ex)
            connection.close()

        except KeyboardInterrupt:
            print("[-] Quitting consumer ...")
            connection.close()


if __name__ == '__main__':
    # @param my_consumer Consumer
    # @param thread_flask Flask Server
    my_consumer = Consumer()
    thread_consumer = Thread(target=my_consumer.main)
    thread_consumer.daemon = True
    thread_consumer.start()
    thread_flask = Thread(target=flask_server.main())



