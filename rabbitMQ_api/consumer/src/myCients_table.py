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





if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')


    """
    def upload_from_pandas(self, dataframe=None, name='table_name_for_df', connect_timeout=350):
        
        Uploads to a mysql table from a pandas dataframe
        Uses sqlalchemy
        Args:
            dataframe: Pandas dataframe with the columns that will be inserted in the database
            name: name of the mysql table to insert the dataframe into
   
        Returns:
            None
   
        """