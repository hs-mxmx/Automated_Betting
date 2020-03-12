

from flask import Flask
app = Flask(__name__)

@app.route('/')
def route_home():
    return 'Group 4 (Flask API) Currently under maintenance'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')