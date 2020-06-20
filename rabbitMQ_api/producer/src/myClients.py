import random
from datetime import datetime
import time
import utils.provider_mapping as pm



class myClients:

    def __init__(self):
        self.name = ""
        self.contentype = ""
        self.content = ""
        self.country = ""
        self.date = ""
        self.price = 0

    def setMapping(self, provider, contentype, content, date, price, country):
        self.name = provider[random.randint(0,len(provider)-1)] 
        self.contentype = contentype[random.randint(0,len(contentype)-1)] 
        self.content = content[random.randint(0,len(content)-1)] 
        self.country = country[random.randint(0,len(country)-1)]
        self.date = date
        self.price = str(random.randint(price[0], price[1]))

    def createClient(self):
        provider = pm.name_class
        contentype = pm.contentype_class
        content = pm.content_class
        date = pm.date_class
        price = [pm.price_class_min, pm.price_class_max]
        country = pm.country_class
        self.setMapping(provider, contentype, content, date, price, country)

    def main(self):
        self.createClient()

