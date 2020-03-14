import pika
import time
import os
import queue
from flask import Flask
from flask import render_template
from datetime import datetime
from threading import Thread

# Create Flask instance
app = Flask(__name__)

# RabbitMQ exchange
EXCHANGE = 'my_exchange'

# Name of rabbitMQ queue
QUEUE = 'my_queue'

# Log file
LOG_FILE = str(datetime.date(datetime.now())) + ".txt"


def main():
    # Location of RabbitMQ server from AMQP_URL variable
    amqp_url =  "amqp://xxalaqou:dQFGDDlp-pfhSolv57XHhVWeqmzcmD6l@crow.rmq.cloudamqp.com/xxalaqou"
    print('URL: %s' % (amqp_url))

    # Stablish connection
    parameters = pika.URLParameters(amqp_url)
    connection = pika.BlockingConnection(parameters) # Connect to CloudAMQP
    try:
        opened_connection(connection) 

    except KeyboardInterrupt:
        print("[-] Quitting consumer ...")
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
    thread = Thread(channel.start_consuming())
    thread.start()

def read_message(msg):
#   print("[+] Reading messages: \n")
    msg = msg.decode("utf-8")
#   q.put(msg)
#   for elem in q.queue: 
    saveFile(LOG_FILE, msg)
    # temp_message = read_tempFile("temp-2020-03-13.txt")
    # print("Messages: %r " % temp_message)
    print("Message: %r " % msg)
    time.sleep(1)
    return

def read_tempFile(logfile):
    my_temp_list = []
    with open(logfile, "r")as my_file: data = my_file.read().replace('\n', ' ')
    my_temp_list = list(data.split(' '))
    return my_temp_list


def saveFile(logfile, msg):
    temp_msg = msg
    msg = "[" + str(datetime.time(datetime.now())) + "]: " + msg
    try:
        file = open(logfile, "a")
        file.write("\n" + msg)
        file.close()
        file_temp = open("temp-"+logfile, "a")
        file_temp.write("\n" + temp_msg)
    except IOError:
        file = open(logfile, "w")
        file.write("\n" + msg)
        file.close()
        file_temp = open("temp-"+logfile, "w")
        file_temp.write("\n" + temp_msg)
    finally:
        file.close()
        file_temp.close()

@app.route('/')
@app.route('/index')
def index():
    temp_message = read_tempFile("temp-2020-03-13.txt")
    print("Messages: %r " % temp_message)
    return render_template('index.html', title='Index', data=temp_message)

@app.route('/home')
def home():
    return render_template('index.html', title='Home', data='Home')

if __name__ == '__main__':
    thread = Thread(target=main)
    thread.daemon = True
    thread.start()
    Thread(target=app.run(debug=True, host='0.0.0.0')).start()