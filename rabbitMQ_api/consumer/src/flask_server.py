from flask import Flask
from flask import render_template
from threading import Thread
from datetime import datetime
import os
import pandas as pd

# Create Flask instance
app = Flask(__name__)

DATE = datetime.now()
LOG_FILE = DATE.strftime('%b_%d_%Y') + ".txt"
LOG_TEMP = "temp-"+ LOG_FILE
LOG_ROUTE  = os.path.abspath(os.curdir) + '/logs/'


@app.route('/')
@app.route('/index')
def index():
    my_clients_list = read_tempFile(LOG_ROUTE + LOG_TEMP)
    # temp_message = read_tempFile(LOG_ROUTE + "temp-Mar_31_2020.txt")
    # print("Messages: %r " % temp_message)
    df = pd.DataFrame(my_clients_list, columns=['Company', 'Price', 'Date'])
    print(df)
    return render_template('index.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route('/home')
def home():
    return render_template('index.html', title='Home', data='Home')


def main():
    Thread(target=app.run(debug=True, host='0.0.0.0')).start()


def read_tempFile(logfile):
    my_temp_list = []
    date_list = []
    price_list = []
    company_list = []
    id_list = []
    result_list = []
    with open(logfile, "r")as my_file: data = my_file.read().replace('\n', ' ')
    my_temp_list = data.split(' ')
    for item in my_temp_list:
        item = item.split('_')
        if len(item) == 4:
            id_list.append(item[0])
            company_list.append(item[1])
            price_list.append(item[2])
            date_list.append(item[3])

    total = len(id_list)
    for _ in range(len(id_list)):
        my_temp_list = []
        # my_temp_list.append(id_list[_])
        my_temp_list.append(company_list[_])
        my_temp_list.append(price_list[_])
        my_temp_list.append(date_list[_])
        result_list.append(my_temp_list)

    return result_list





