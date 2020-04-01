import smtplib

from string import Template
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
BACKUP_ROUTE=os.getenv('BACKUP_ROUTE')
BACKUP= [file for file in os.listdir(BACKUP_ROUTE) if os.path.isfile(os.path.join(BACKUP_ROUTE, file))]

# Current Date
DATE = datetime.now()
# Log file
LOG_FILE = DATE.strftime('%b_%d_%Y') + ".txt"

def contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """
    names = []
    emails = []
    try:
        print(os.getcwd())
        with open('utils/'+filename, 'r') as contacts_file:
            for contact in contacts_file:
                names.append(contact.split()[0])
                emails.append(contact.split()[1])
        return names, emails
    except:
        print("No file called ",filename," was found...")
        exit

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    try:
        with open(filename, 'r') as template_file:
            template_file_content = template_file.read()
        return Template(template_file_content)
    except:
        print("No file called ",filename," was found...")
        exit

def main():
    while True:
        BACKUP= [file for file in os.listdir(BACKUP_ROUTE) if os.path.isfile(os.path.join(BACKUP_ROUTE, file))]
        if LOG_FILE in BACKUP:
            break
        initializeBackup()
        time.sleep(1)
    exit


def myEventHandler():
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = initializeBackupEvent
    return my_event_handler


def myObserver():
    path = "."
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(myEventHandler(), path, recursive=go_recursively)
    my_observer.start()
    try: main()
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()


def initializeBackupEvent(event):
    initializeBackup()

def initializeBackup():
    if LOG_FILE not in BACKUP:
        names, emails = contacts('my_contacts.txt') # read contacts
        message_template = read_template('logs/' + LOG_FILE)
        log_file = open('logs/'+LOG_FILE, "r").read()
        backup_file = open(BACKUP_ROUTE+LOG_FILE,"w+")
        backup_file.write(str(log_file))

        # set up the SMTP server
        s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
        s.starttls()
        MY_ADDRESS=os.getenv('OU_USER')
        PASSWORD=os.getenv('OU_PASS')
        s.login(MY_ADDRESS, PASSWORD)

        # For each contact, send the email:
        for name, email in zip(names, emails):
            msg = MIMEMultipart()       # create a message

            # add in the actual person name to the message template
            message = message_template.substitute(PERSON_NAME=name.title())

            # setup the parameters of the message
            msg['From']=MY_ADDRESS
            msg['To']=email
            msg['Subject']=LOG_FILE
            
            # add in the message body
            msg.attach(MIMEText(message, 'plain'))
            
            # send the message via the server set up earlier.
            s.send_message(msg)
            del msg
            
        # Terminate the SMTP session and close the connection
        s.quit()

if __name__ == '__main__':
    main()