from __future__ import print_function
import mysql.connector
import os
import re
import datetime
import itertools
from mysql.connector import errorcode
from dotenv import load_dotenv
from pathlib import Path

class dbConnection():

    def __init__(self):
        self.user = ''
        self.password = ''
        self.host = ''
        self.database = ''
        self.cursor = ''
        self.table = ''
        self.connection = ''


    def enableConnection(self, data):
        if self.user == '':
            # print("Finding credentials...") 
            self.readEnv()
        self.stablishConnection(data)
    

    def readEnv(self):
        """
        Read environment variables from .env file
        """
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        self.user=os.getenv("USER")
        self.password=os.getenv("PASSWORD")
        self.host=os.getenv("HOST")
        self.database=os.getenv("DATABASE")
        self.table=os.getenv("MYTABLE")

    
    def stablishConnection(self, data):
        """
        MYSQL connection handler automated in order to
        be deployed successfully via Docker
        """
        try:
            self.connection = mysql.connector.connect(user=self.user, password=self.password,
                                                host=self.host)
            # print("Connection Stablished as {} ".format(self.user))
            self.cursor =  self.connection.cursor(buffered=True)
            self.checkDataBase(self.database)
            self.checkTable(self.table)
            self.insertTuples(data)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            self.cursor.close()
            self.connection.close()


    def checkDataBase(self, dataBase):
        """
        Query to check and create if env database exists or not
        """
        data_query = """CREATE DATABASE IF NOT EXISTS `%s`;""" %(dataBase)
        base_query = """USE `%s`;""" % (dataBase)
        try:
            self.cursor.execute(data_query)
            # print("Connecting to {} ...".format(dataBase))
            self.cursor.execute(base_query)
        except mysql.connector.Error as err:
            print(err)
        else:
            pass
            # print("Database {} was created succesfully!".format(dataBase))


    def checkTable(self, tableName):
        """
        Query to check and create if env tablename exists or not
        """
        TABLES = {}
        TABLES[tableName] = (
        "CREATE TABLE IF NOT EXISTS `clients` ("
        # "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `name` varchar(16) NOT NULL,"
        "  `price` varchar(16) NOT NULL,"
        "  `date` date NOT NULL"
        #"  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")
        myTable_description = TABLES[tableName]
        try:
            # print("Creating table {}: ".format(tableName))
            self.cursor.execute(myTable_description)
        except mysql.connector.Error as err:
            pass
            # print(err.msg)
        else:
            pass
            # print("Table {} was created succesfully!".format(tableName))
        self.table = tableName
        

    def insertTuples(self, data):
        """
        Query to insert tuples from consumer
        """
        data = self.formatInfo(data)
        # print(data)
        self.cursor.execute("""INSERT INTO `%s` (name, price, date) VALUES ('%s', '%s' , '%s') ;""" %(self.table, data[1], data[2], data[3],))
        self.connection.commit()
        print("Data inserted successfully: {}".format(data))
        

    def getData(self, tableName):
        """
        Query to get tuples from env table name
        """
        print(tableName)
        self.readEnv()
        self.connection = mysql.connector.connect(user=self.user, password=self.password,
                                                host=self.host,
                                                database=self.database)
        self.cursor =  self.connection.cursor()
        self.cursor.execute("""SELECT * FROM `%s` ;""" %(tableName))
        raw_data = self.cursor.fetchall()
        myData = list(itertools.chain(*raw_data))
        for item in myData: print(item)
                

    def formatInfo(self, data):
        """
        Method to format info received from producer in order
        to be stored into the database
        """
        replace_strings = {"_" : " ", "(" : "", ")" : ""}
        myData = []
        for i, j in replace_strings.items():
            data = data.replace(i, j)
        myData = data.split(' ')
        return myData
        

if __name__ == "__main__":
    mySQL = dbConnection()
    mySQL.enableConnection("0_Telefonica_208_(2020-03-14)")
