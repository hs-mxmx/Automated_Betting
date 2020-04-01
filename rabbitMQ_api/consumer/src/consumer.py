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

# Create Flask instance
app = Flask(__name__)

# readEnv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
EXCHANGE=os.getenv("EXCHANGE")
QUEUE=os.getenv("QUEUE")
AMQP_URL=os.getenv("AMQP_URL")
MYTABLE=os.getenv("MYTABLE")
BACKUP_ROUTE=os.getenv("BACKUP_ROUTE")

# Current Date
DATE = datetime.now()

# Log file
LOG_FILE = DATE.strftime('%b_%d_%Y') + ".txt"
LOG_TEMP = "temp-"+ LOG_FILE

# Docker Log Route
# LOG_ROUTE = os.path.dirname(__file__) + '/logs/'

""" TROUBLESHOOTING """
# Windows alternative Route
LOG_ROUTE = os.path.abspath(os.curdir) + '/logs/'

# Only for Docker Image (Linux)
# LOG_ROUTE = os.path.dirname(os.path.relpath(__file__)) + '/logs/'

def main():
    # Location of RabbitMQ server from AMQP_URL variable
    # amqp_url = os.environ['AMQP_URL']
    # if amqp_url=='':amqp_url =  "amqp://xxalaqou:dQFGDDlp-pfhSolv57XHhVWeqmzcmD6l@crow.rmq.cloudamqp.com/xxalaqou"
    amqp_url=os.getenv('AMQP_URL')

    # Stablish connection
    parameters = pika.URLParameters(amqp_url)
    connection = pika.BlockingConnection(parameters) # Connect to CloudAMQP
    try:
        opened_connection(connection) 

    except KeyboardInterrupt:
        print("[-] Quitting consumer ...")
        connection.close()


def opened_connection(connection):
    """Connection stablished"""
    channel = connection.channel()
    opened_qos(channel,connection)


def opened_qos(channel, connection):
    """QoS Queue"""
    channel.basic_qos(prefetch_count=1, 
    callback=opened_queue(channel,connection))


def opened_queue(channel, connection):
    """Opened Queue"""
    channel.queue_bind(queue=QUEUE, exchange= '', routing_key=QUEUE, callback=open_message(channel, connection))


def callback(ch, method, properties, body):
    read_message(body)


def open_message(channel, connection):
    channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)
    print("Waiting for messages...")
    thread = Thread(channel.start_consuming())
    thread.start()


def read_message(msg):
    msg = msg.decode("utf-8")
    saveFile(msg)
    print("Message: %r " % msg)
    time.sleep(1)
    return


def saveFile(msg):
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
        if(str(datetime.now().hour)+':'+str(datetime.now().minute)=='21:44'):
            if(int(datetime.now().second)>=0 and int(datetime.now().second)<=59):
                Thread(target=informer.main()).start()

    except IOError:
        file = open(LOG_ROUTE + LOG_FILE, "w+")
        file.write("\n" + msg)
        file.close()
        file_temp = open(LOG_ROUTE + LOG_TEMP, "w+")
        file_temp.write("\n" + temp_msg)
        file_temp.close()
        
        

@app.route('/')
@app.route('/index')
def index():
    temp_message = read_tempFile(LOG_ROUTE + "temp-Mar_31_2020.txt")
    # print("Messages: %r " % temp_message)
    return render_template('index.html', title='Index', data=temp_message)


@app.route('/home')
def home():
    return render_template('index.html', title='Home', data='Home')


if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    log.disabled = True
    thread = Thread(target=main)
    thread.daemon = True
    thread.start()
    Thread(target=app.run(debug=True, host='0.0.0.0')).start()




# def read_tempFile(logfile):
#     my_temp_list = []
#     with open(logfile, "r")as my_file: data = my_file.read().replace('\n', ' ')
#     my_temp_list = list(data.split(' '))
#     return my_temp_list