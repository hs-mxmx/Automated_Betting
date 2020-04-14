from flask import Flask
from flask import render_template
from threading import Thread

# Create Flask instance
app = Flask(__name__)



@app.route('/')
@app.route('/index')
def index():
    # temp_message = read_tempFile(LOG_ROUTE + "temp-Mar_31_2020.txt")
    # print("Messages: %r " % temp_message)
    return render_template('index.html', title='Index', data=temp_message)


@app.route('/home')
def home():
    return render_template('index.html', title='Home', data='Home')


def main():
    Thread(target=app.run(debug=True, host='0.0.0.0')).start()







