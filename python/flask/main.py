from flask import Flask,Response
from flask_socketio import SocketIO, send, emit
import sys
sys.path.insert(0, '../i2c')
from imu import run_imu
from oled import init_oled,write_all
import eventlet
import time,datetime
import random

eventlet.monkey_patch()

header = '-([Glove 2 Gesture])-'
data = []
connectedClients = 0



app = Flask(__name__)
#app.config['SECRET_KEY'] = 'thisistnkgtgsecretkey#'
socketio = SocketIO(app)

@socketio.on('connect', namespace='/web')
def on_connect():
    #connectedClients += 1
    
    print('Client Connected')
    
@socketio.on('disconnect', namespace='/web')
def on_disconnect():
    #connectedClients -= 1
    print('Client Disconnected')
    
@socketio.on('ping', namespace='/web')
def on_ping():
    print("GOT PING :D :) :P ==========")
    socketio.emit('pong','This is pong :)', namespace='/web')

def dummy_accgyro():
    return [i for i in range(6)]
def dummy_mag():
    return [i for i in range(3)]
def dummy_flex():
    return [i*100 for i in range(5)]

def loop_input():
    thread_oled = None
    thread_livedata = None
    start = datetime.datetime.now()
    while True:
        data = run_imu(start)
        thread_oled = eventlet.spawn_n(loop_oled,data)
        thread_livedata = eventlet.spawn_n(loop_livedata,data)
        print(data)
        time.sleep(0.02)
        eventlet.kill(thread_oled)
        eventlet.kill(thread_livedata)
        start = datetime.datetime.now()
        
def loop_livedata(data):
    dataset = data + dummy_flex()
    socketio.emit('livedata', { 'msg': dataset } , namespace='/web')

def loop_oled(data):
    write_all([header,','.join(str(round(i)) for i in data[:3]),','.join(str(round(i)) for i in data[3:6]),','.join(str(round(i)) for i in data[6:9]),"Good Luck"])

def callback(gt, *args, **kwargs):
    """ this function is called when results are available """
    result = gt.wait()
    print(result)


@app.route('/')
def index():
    print(data)
    return "Hello World"

if __name__ == '__main__':
    thread_input = eventlet.spawn(loop_input)
    #thread_input.link(callback)
    
    
    print('RUNNING')
    socketio.run(app,host= '0.0.0.0',port='3000', debug=True)

