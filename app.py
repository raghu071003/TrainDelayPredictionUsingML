from flask import Flask, render_template, request
from data_manager import *
from trainp import*
from time import sleep

# Flask app (app.py)
from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_delay', methods=['POST'])
def get_delay():
    station = request.form['station']
    train = request.form['train']
    date = request.form['date']
    result = subprocess.check_output(['python', 'tainp.py', station, train, date])
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
