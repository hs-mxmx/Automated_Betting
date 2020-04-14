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

class Informer:

    def contacts(self, filename):
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


    def read_template(self, filename):
        try:
            with open(filename, 'r') as template_file:
                template_file_content = template_file.read()
            return Template(template_file_content)
        except:
            print("No file called ",filename," was found...")
            exit


    def main(self):
        while True:
            BACKUP= [file for file in os.listdir(BACKUP_ROUTE) if os.path.isfile(os.path.join(BACKUP_ROUTE, file))]
            if LOG_FILE in BACKUP:
                break
            self.initializeBackup()
            time.sleep(1)
        exit


    def initializeBackup(self):
        if LOG_FILE not in BACKUP:
            names, emails = self.contacts('my_contacts.txt')
            message_template = self.read_template('logs/' + LOG_FILE)
            log_file = open('logs/'+LOG_FILE, "r").read()
            backup_file = open(BACKUP_ROUTE+LOG_FILE,"w+")
            backup_file.write(str(log_file))

            # set up the SMTP server
            s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
            s.starttls()
            MY_ADDRESS=os.getenv('OU_USER')
            PASSWORD=os.getenv('OU_PASS')
            s.login(MY_ADDRESS, PASSWORD)

            for name, email in zip(names, emails):
                msg = MIMEMultipart()       
                message = message_template.substitute(PERSON_NAME=name.title())

                msg['From']=MY_ADDRESS
                msg['To']=email
                msg['Subject']=LOG_FILE
                msg.attach(MIMEText(message, 'plain'))
                
                s.send_message(msg)
                del msg
                
            s.quit()


if __name__ == '__main__':
    my_informer = Informer()
    my_informer.main()


"""
Monitorize Functions
"""

# def myEventHandler():
#     """
#     Returns an Event Handler in order to monitorize the
#     files created on backup to send the mail in case of delay
#     """
#     patterns = "*"
#     ignore_patterns = ""
#     ignore_directories = False
#     case_sensitive = True
#     my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
#     my_event_handler.on_created = initializeBackupEvent
#     return my_event_handler


# def myObserver():
#     """
#     Observer thread created to monitorize the event referenced on
#     my EventHandler on created function
#     """
#     path = "."
#     go_recursively = True
#     my_observer = Observer()
#     my_observer.schedule(myEventHandler(), path, recursive=go_recursively)
#     my_observer.start()
#     try: main()
#     except KeyboardInterrupt:
#         my_observer.stop()
#         my_observer.join()


# def initializeBackupEvent(event):
#     initializeBackup()