from __future__ import print_function
import mysql.connector
import os
import re
import datetime
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
            print("Finding credentials...") 
            self.readEnv()
        self.stablishConnection(data)
    

    def readEnv(self):
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        self.user=os.getenv("USER")
        self.password=os.getenv("PASSWORD")
        self.host=os.getenv("HOST")
        self.database=os.getenv("DATABASE")

    
    def stablishConnection(self, data):
        try:
            self.connection = mysql.connector.connect(user=self.user, password=self.password,
                                                host=self.host,
                                                database=self.database)
            print("Connection Stablished as {} ".format(self.user))
            self.cursor =  self.connection.cursor()
            self.checkTable()
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


    def createTable(self, tableName):
        TABLES = {}
        TABLES[tableName] = (
        "CREATE TABLE `clients` ("
        # "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `name` varchar(16) NOT NULL,"
        "  `price` varchar(16) NOT NULL,"
        "  `date` date NOT NULL"
        #"  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")

        myTable_description = TABLES[tableName]
        try:
            print("Creating table {}: ".format(tableName))
            self.cursor.execute(myTable_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("Table {} was created succesfully!".format(tableName))
        self.table = tableName


    def checkTable(self):
        self.cursor.execute("""SHOW TABLES""")
        print("=== TABLES === \n")
        for (table,) in self.cursor: print("[+] {} \n".format(table))
        # temp_table = input("Select your table: ")
        temp_table = 'clients'
        self.table = temp_table
        try:
            self.cursor.execute("""SELECT * FROM `%s` ;""" %(self.table,))
            print(self.cursor.fetchall())
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table already exists.")
            else:
                print(err.msg)
            mytable = input("Insert table name: ")
            self.createTable(mytable)


    def insertTuples(self, data):
        data = self.formatInfo(data)
        print(data)
        self.cursor.execute("""INSERT INTO `%s` (name, price, date) VALUES ('%s', '%s' , '%s') ;""" %(self.table, data[1], data[2], data[3],))
        self.connection.commit()
        
        
#INSERT INTO clients (id, name, price, date) VALUES ('2','hola','400','2020-03-14');


    def formatInfo(self, data):
        replace_strings = {"_" : " ", "(" : "", ")" : ""}
        myData = []
        for i, j in replace_strings.items():
            data = data.replace(i, j)
        myData = data.split(' ')
        return myData

#if __name__ == "__main__":
    #mySQL = dbConnection()
    #mySQL.formatInfo("0_Telefonica_208_(2020-03-14)")
    #mySQL.enableConnection()
