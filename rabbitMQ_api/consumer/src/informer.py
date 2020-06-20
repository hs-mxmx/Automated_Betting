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
import utils.consumer_mapping as cm
import time

class Informer:

    def init(self):
        self.file = ''
        self.backup_route = ''
        self.backup = ''
        self.send = ''
        self.check = False


    def contacts(self, filename):
        # @param filename String
        names = []
        emails = []
        try:
            print(os.getcwd())
            file_route = cm.UTILS_ROUTE + filename
            with open(file_route, 'r') as contacts_file:
                for contact in contacts_file:
                    names.append(contact.split()[0])
                    emails.append(contact.split()[1])
            return names, emails
        except Exception as ex:
            print("No file called ",filename," was found...")
            print(ex)
            exit


    def read_template(self, filename):
        # @param filename String
        try:
            with open(filename, 'r') as template_file:
                template_file_content = template_file.read()
            return Template(template_file_content)
        except:
            print("No file called ",filename," was found...")
            exit


    def main(self, send_mail):
        self.send = send_mail
        if self.send == True:
            env_path = Path('.') / cm.ENV
            load_dotenv(dotenv_path=env_path)
            self.file = datetime.now().strftime(cm.DATE_FORMAT) + cm.TXT
            self.backup_route = os.getenv(cm.BACKUP_ROUTE)
            self.backup = [file for file in os.listdir(self.backup_route) if os.path.isfile(os.path.join(self.backup_route, file))]
            while True:
                if self.file in self.backup:
                    break
                self.initializeBackup()
                time.sleep(1)
        else:
            print("Exiting informer")
            exit


    def initializeBackup(self):
        if self.file not in self.backup and self.send:
            print("CHECK DONE")
            self.send = False
            my_contacts = cm.CONTACTS_ROUTE + cm.TXT
            log_file = cm.LOGS + self.file
            names, emails = self.contacts(my_contacts)
            message_template = self.read_template(cm.LOGS + self.file)
            log_file = open(log_file, "r").read()
            backup_file = open(self.backup_route + self.file,"w+")
            backup_file.write(str(log_file))

            # set up the SMTP server
            s = smtplib.SMTP(host=cm.SMTP_HOST, port=cm.SMTP_PORT)
            s.starttls()
            MY_ADDRESS=os.getenv('OU_USER')
            PASSWORD=os.getenv('OU_PASS')
            s.login(MY_ADDRESS, PASSWORD)
            print("SENDING MAIL")

            for name, email in zip(names, emails):
                msg = MIMEMultipart()       
                message = message_template.substitute(PERSON_NAME=name.title())

                msg['From']=MY_ADDRESS
                msg['To']=email
                msg['Subject']=self.file
                msg.attach(MIMEText(message, 'plain'))
                
                s.send_message(msg)
                del msg
                
            s.quit()


if __name__ == '__main__':
    my_informer = Informer()
    my_informer.main(True)


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