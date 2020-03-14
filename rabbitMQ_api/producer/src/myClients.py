import random
from datetime import datetime
import time



class myClients:

    def __init__(self, id, company, date, price):
        self.id = id
        self.company = company
        self.date = date
        self.price = price

    def createClient(self):
        self.date = str(datetime.date(datetime.now()))
        self.price = random.randint(100,700)
        if self.id == 0:
            self.company = 'Telefonica'
        if self.id == 1:
            self.company = 'Google'
        if self.id == 2:
            self.company = 'Apple'
        if self.id == 3:
            self.company = 'Tesla'
        if self.id == 4:
            self.company = 'NASA'
        if self.id == 5:
            self.company = 'Microsoft'

    def main(self):
        self.createClient()

        