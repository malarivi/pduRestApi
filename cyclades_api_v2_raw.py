'''
Use Flask API to interface Cyclades PDU via serial port

First iteration where data is passed raw to and from the serial port to the Flask API instantaneously.
This works great for basic testing of the workflow and as a basic framework for REST <-> Console communications.

Run with   export FLASK_APP=cyclades.py flask run

Serial port permissions may be missing, fix with usermod -a -G dialout $USER
'''

import serial
import re
import sys
import time
from flask import Flask

username = 'admin'
password = 'pm8'
serialIf = '/dev/ttyUSB0'

app = Flask(__name__)
console = serial.Serial(port=serialIf)

def read_serial(console):
    '''
    Check if there is data waiting to be read
    Read and return it.
    else return null string
    '''
    data_bytes = console.inWaiting()
    if data_bytes:
        return console.read(data_bytes)
    else:
        return ""


def check_logged_in(console):
    '''
    Check if logged in to device
    '''
    console.write('\n')
    time.sleep(1)
    prompt = read_serial(console)
    if '>' in prompt or '#' in prompt:
        return True
    else:
        return False


def login(console):
    '''
    Login to device
    '''
    login_status = check_logged_in(console)
    if login_status:
        print "Already logged in"
        return None

    print 'Initializing Cyclades PDU Login'
    while True:
        console.write('\n')
        time.sleep(1)
        input_data = read_serial(console)
        if not 'Username' in input_data:
            continue
        console.write(username + '\n')
        time.sleep(1)

        input_data = read_serial(console)
        if not 'Password' in input_data:
            continue
        console.write(password + '\n')
        time.sleep(1)

        login_status = check_logged_in(console)
        if login_status:
            print "Successfully attached to Cyclades PDU\n"
            break


def logout(console):
    '''
    Exit from console session
    '''
    while check_logged_in(console):
        console.write('exit\n')
        time.sleep(.5)

    print "Successfully detached from Cyclades PDU"


def send_command(console, cmd=u''):
    '''
    Send a command, strip the input characters and return line from output
    '''
    console.write(cmd + '\n')
    time.sleep(1)
    return read_serial(console)[len(cmd):-3]
    '''return read_serial(console) fallback with send output'''

@app.route('/system')
def ver():
    login(console)
    return send_command(console, cmd='ver')

@app.route('/system/<something>')
def apiexec(something):
    print("GET Request: \"" + something + "\"")
    byteEncoder = something.encode()
    login(console)
    return send_command(console, cmd=byteEncoder)

@app.route('/test')
    print("Prints output to Flask console")
    return "Prints output to GET Request \n"

@app.route('/system/state')
def apistate():
    return 
    return send_command(console, cmd='status all')

@app.route('/pkill')
def pkill():
    sys.exit()

@app.route('/system/reboot')
def apideny():
    denied = "Illegal GET Request denied."
    print(denied)
    return denied + "\n"
