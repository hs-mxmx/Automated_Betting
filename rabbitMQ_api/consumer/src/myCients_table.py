from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd


app = Flask(__name__)

myData = {"Name":'Telefonica', "Total Price":'1000', "Total Number": '2'}

df = pd.DataFrame({'Name': [myData.get("Name",'')],
                   'Total Price': [myData.get("Total Price",'')],
                   'Total number': [myData.get("Total Number",'')]})


@app.route('/', methods=("POST", "GET"))
def html_table():

    return render_template('table.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

class myClients_table:

    def __init__()




if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')