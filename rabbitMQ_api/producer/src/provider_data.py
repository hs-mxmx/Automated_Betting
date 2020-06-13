
import utils.provider_mapping as pm
import random
import os
import json

class Provider:


    def __init__(self):
        self.name = ""
        self.country = ""
        self.content = ""
        self.contentype = ""
        self.date = ""
        self.metadata = ""
        self.new = True
        super().__init__()


    def getData(self, data_class):
        return random.randint(0, len(data_class)-1)


    def setData(self):
        if self.new:
            pm.NAME = pm.name_class[self.getData(pm.name_class)]
            self.name = pm.NAME
            self.new = False
        pm.CONTENT = pm.content_class[self.getData(pm.content_class)]
        pm.CONTENTYPE = pm.contentype_class[self.getData(pm.contentype_class)]
        pm.COUNTRY = pm.country_class[self.getData(pm.country_class)]
        pm.DATE = pm.date_class
        self.country = pm.COUNTRY
        self.content = pm.CONTENT
        self.contentype = pm.CONTENTYPE
        self.date = pm.DATE


    def generate_data(self):
            name = self.name
            country = self.country
            date = self.date
            content = self.content
            contenType = self.contentype
            
            metaData = {
                        "name": name,
                        "country": country,
                        "date": date,
                        "content": content,
                        "contenType": contenType
            }

            self.name = name

            return metaData


    def generate_metaData(self):
        array_compressed = []
        total_metadata = random.randint(1,20)
        for data in range(total_metadata):
            self.setData()
            metaData = self.generate_data()
            array_compressed.append(metaData)

        self.new = True
        return array_compressed


    def generate_provider(self):
        self.setData()
        provider_data = { 
            self.name: {
                "Metadata": self.generate_metaData()
            }
        }
        self.generate_file(provider_data)
        self.metadata = (self.name + "_" + self.country + "_(" + self.date + ")_" \
                + self.contentype + "_" + self.content)
        
        return self.metadata
        



    def set_data_environment(self, data, type):
        try:
            os.environ["{}".format(type)] = data
        except:
            pass


    def generate_file(self, provider_data):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        print(current_dir)
        file = (self.name + '_' + self.date + '_1' + pm.FILE_EXTENSION)
        path = (current_dir + '/utils/catalogues/' + self.name + '/')
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
        try:
            if os.path.exists(path + file):
                file = file.split('_')
                provider = file[0]
                date = file[1]
                id = file[2]
                id = id.split(pm.FILE_EXTENSION)
                new_id = '_' + str(int(id[0]) + 1)
                new_file = (provider + '_' + date + new_id + pm.FILE_EXTENSION)
                while os.path.exists(path + new_file):
                    new_file = self.check_file(path, new_file)
                return new_file
            return file
        except Exception as ex:
            print(ex)
            pass
        
            

_ = 0

my_provider = Provider()
msg = my_provider.generate_provider()