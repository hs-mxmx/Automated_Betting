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


    def enableConnection(self, data, provider):
        # @param data Array
        # @param provider String
        if self.user == '':
            env_path = Path('.') / '.env'
            load_dotenv(dotenv_path=env_path)
            self.user=os.getenv("USER")
            self.password=os.getenv("PASSWORD")
            self.host=os.getenv("HOST")
            self.database=os.getenv("DATABASE")
            self.table=provider.upper()
        self.stablishConnection(data)


    def stablishConnection(self, data):
        # @param data Array
        """
        MYSQL connection handler automated in order to
        be deployed successfully via Docker
        """
        try:
            self.connection = mysql.connector.connect(user=self.user, password=self.password,
                                                host=self.host)
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
        # @param dataBase String
        """
        Query to check and create if env database exists or not
        """
        data_query = """CREATE DATABASE IF NOT EXISTS `%s`;""" %(dataBase)
        base_query = """USE `%s`;""" % (dataBase)
        try:
            self.cursor.execute(data_query)
            self.cursor.execute(base_query)
        except mysql.connector.Error as err:
            print(err)
        else:
            pass


    def checkTable(self, tableName):
        # @param tableName String
        """
        Query to check and create if env tablename exists or not
        """
        TABLES = {}
        TABLES[tableName] = (
        "CREATE TABLE IF NOT EXISTS `%s` ("
        # "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `name` varchar(16) NOT NULL,"
        "  `date` date NOT NULL,"
        "  `contentType` varchar(16) NOT NULL,"
        "  `content` varchar(16) NOT NULL,"
        "  `country` varchar(16) NOT NULL,"
        "  `price` int(11) NOT NULL"
        #"  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")%(tableName)
        myTable_description = TABLES[tableName]
        try:
            self.cursor.execute(myTable_description)
        except mysql.connector.Error:
            pass
        else:
            pass
        self.table = tableName
        

    def insertTuples(self, data):
        # @param data Array
        """
        Query to insert tuples from consumer
        """
        self.cursor.execute("""INSERT INTO `%s` (name, date, contentType, content, country, price) VALUES ('%s', '%s' , '%s', '%s', '%s', '%s') ;""" %(self.table, data[0], data[1], data[2], data[3], data[4], data[5]))
        self.connection.commit()
        # print("Data inserted successfully: {}".format(data))
        

    def getData(self, tableName):
        # @param tableName String
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
        

if __name__ == "__main__":
    mySQL = dbConnection()
    mySQL.enableConnection(["Test", '2020-06-17', "Test", "Test", "Test"], 'IBM')


