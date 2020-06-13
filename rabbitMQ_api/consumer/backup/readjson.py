
import json
import random
import os

# msg = "telefonica_spain_(2020-06-26)_TV_Show"

import utils.provider_data as prov

class GenerateCatalogue:

    def __init__(self):
        super().__init__()

    def generate_data(self):
        name = os.environ["PROVIDER"]
        country = os.environ["COUNTRY"]
        date = os.environ["DATE"]
        content = os.environ["CONTENT"]
        contenType = os.environ["CONTENTYPE"]
        
        metaData = {
                    "name": name,
                    "country": country,
                    "date": date,
                    "content": content,
                    "contenType": contenType
        }

        os.environ["PROVIDER"] = name

        return metaData

    def generate_metaData(self):
        array_compressed = []
        total_metadata = random.randint(0,20)
        for data in range(total_metadata):
            metaData = self.generate_data()
            array_compressed.append(metaData)

        return array_compressed

    def generate_provider(self, msg):
        new_msg = msg.split('_')
        self.set_data_environment(new_msg[0], "PROVIDER")
        self.set_data_environment(new_msg[1], "COUNTRY")
        self.set_data_environment(new_msg[2], "DATE")
        self.set_data_environment(new_msg[3], "CONTENT")
        self.set_data_environment(new_msg[4], "CONTENTYPE")
        provider_data = { 
            os.environ["PROVIDER"]: {
                "Metadata": self.generate_metaData()
            }
        }

        try:
            with open('result.json', 'a') as jsonfile:
                json.dump(provider_data, jsonfile, indent=4, separators=(',', ': '), sort_keys=True)
                
        except:
            pass

        return provider_data



    def set_data_environment(self, data, type):
        try:
            os.environ["{}".format(type)] = data
        except:
            pass


provider = prov.Provider()
msg = provider.generate_provider()

myJson = GenerateCatalogue()
myJson.generate_provider(msg)




