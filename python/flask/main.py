# Import standard libs
import sys
import time
import datetime
import random
import json
import numpy as np
from os import getpid

# Import threading libs
import eventlet
eventlet.monkey_patch()

# Import Flask libs
from flask import Flask, Response, request, jsonify
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from flask_pymongo import PyMongo
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# Import I2C modules
sys.path.insert(0, '../i2c')
from imu import IMU
from mux import SW
from oled import display
 
# Import ML modules
enableML = False
if enableML:
    sys.path.insert(0, '../predict')
    from predict import Model
    model = Model()

# Import DB libs
from models import Gesture, Pose, Movement, Step


# VARIABLES
# smallest possible difference
EPSILON = sys.float_info.epsilon
# Connected Socket Clients
connectedClients = 0
# OLED Header
header = '-([Glove 2 Gesture])-'

# Size of sample/second
sampleRate = 20
# Period of capturing each sample
samplePeriod = 1.0/sampleRate
# Size of window to slide with samples
windowSize = 10
# Input size 3:Ac, 6:AcGy, 9:AGM, 12:AGMF
inputSize = 6
# Sliding window of data
datas = []
# Average of datas
avgData = []
# Difference between new data and avgData
diff = []
# Average Moving data since start moving to stop moving
movingData = []
# Threshold which one of each value considered as start moving
threshold = 20
# MUX Channels
imu_mux = []
main_mux_channel = 1

# Boolean if model is loaded
model_isloaded = True

# _____________________________ SOCKET.IO Handlers __________________________________


@socketio.on('connect', namespace='/web')
def on_connect():
    global connectedClients
    connectedClients += 1
    print(getpid(), 'Client Connected')


@socketio.on('disconnect', namespace='/web')
def on_disconnect():
    global connectedClients
    connectedClients -= 1
    print(getpid(), 'Client Disconnected')


@socketio.on('ping', namespace='/web')
def on_ping():
    print(getpid(), "GOT PING :D :) :P ==========")
    socketio.emit('pong', 'This is pong :)', namespace='/web')


@socketio.on('resample', namespace='/web')
def on_resample(gestures, size):
    print(getpid(), "Resampling...", size)
    for ges in gestures:
        if(len(gestures[ges][0]) > size):
            # Resample
            for attr in range(len(gestures[ges])):
                delta = (len(gestures[ges][attr])-1) / float(size-1)
                mapped = [interpolate(gestures[ges][attr], i*delta)
                          for i in range(size)]
                gestures[ges][attr] = mapped
    socketio.emit('resampled', gestures, namespace='/web')

@socketio.on('predict', namespace='/web')
def on_predict(data):
    if enableML:
        global model
        result, time_send = model.predictImu([data], None)
        print(getpid(), time_send, result)
        if display != None:
            display.write_row(text=str(result[0]))
        socketio.emit('predict_result', str(result[0]), namespace='/web')

# _____________________________ Flask __________________________________


@app.route('/')
@app.route('/api')
def index():
    return "Hello World"

@app.route('/gestures')
def get_gestures():
    pose_col = Pose._get_collection()
    ges_col = Gesture._get_collection()

    # step1 = Step(pose=Pose.objects.first(), movement=Movement.objects.first())
    # print(getpid(),step1)
    # gesture = Gesture(name="GumGesture", steps=[step1, step1])
    # print(getpid(),gesture)
    # gesture.save()
    gestures = Gesture.objects

    return str([i.to_json() for i in gestures])

# _____________________________ Functions __________________________________


def interpolate(arr, fi):
    i = int(fi)
    f = fi - i

    if f >= EPSILON or f == 0:
        return arr[i]
    else:
        return arr[i] + f*(arr[i+1]-arr[i])


def angle_diff(unit1, unit2):
    phi = abs(unit2-unit1) % 360
    sign = 1
    # used to calculate sign
    if not ((unit1-unit2 >= 0 and unit1-unit2 <= 180) or (
            unit1-unit2 <= -180 and unit1-unit2 >= -360)):
        sign = -1
    if phi > 180:
        result = 360-phi
    else:
        result = phi

    return result*sign


def dummy_imu():
    return [0 for i in range(9)]


def dummy_accgyro():
    return [0 for i in range(6)]


def dummy_mag():
    return [0 for i in range(3)]


def dummy_flex():
    return [0 for i in range(5)]

# _____________________________ THREAD/LOOP/BG ____________________________


def loop_input():
    global datas
    print(getpid(), "Starting input loop...")
    
    data_record = []
    data_back = []
    sampleRate = 20
    record = False
    first = True
    while True:
        data = [[] for i in imu_mux]
        data_ori = [[] for i in imu_mux]
        starttime = [datetime.datetime.now() for i in imu_mux]
        for i, cur_imu in enumerate(imu_mux):
            # Switch mux channel & Read data
            try:
                SW.channel(cur_imu.get_channel())
                startnow = starttime[i]
                starttime[i] = datetime.datetime.now()

                data[i] = cur_imu.get_all(starttime[i])
                data[i] = [round(data[i][j],3) for j in range(9)]
                data_ori[i] = data[i][:]

                
        
                if(i != 0):
                    data[i][:3] = [angle_diff(data[i][j], data[0][j])
                                   for j in range(3)]

            except (Exception):
                print("Get channel fail #", cur_imu.get_channel())
                data[i] = dummy_imu()
                try:
                    cur_imu.enable()
                    time.sleep(2)
                except (Exception):
                    print("MUX fail #", cur_imu.get_channel())
                    
            print("Channel#", cur_imu.get_name(), data[i][:6])

            # # Calculation
            # if len(datas) > windowSize:
            #     eventlet.spawn_n(background_process_accel, data)
            #     datas = datas[1:]
            # datas.append(data)

        # # Export Data through socket/oled
        # # fill the missing imu
        data = data + [dummy_imu() for i in range(len(data), 6)]
        
        data_numpy = np.array(data,np.float64)
        data_numpy = data_numpy[:,0:3]
        data_back.append(data_numpy)
        data_different = []
        if first:
            old_data = data_numpy
            first = False
        if not record and len(data_back) > 2:
            compare =[angle_diff(old_data[i][j],data_numpy[i][j]) for j in range(len(old_data[i])) for i in range(len(old_data))]
            compare = np.array(compare,np.float64)
            if not (compare < threshold).all():

                data_record = []
                data_record = data_back[:]
                record = True
        elif record and len(data_record) < sampleRate: 
            data_record.append(data_numpy)
        elif record and len(data_record) == sampleRate:
            data_different = data_record
            """
            for i in range (1,len(data_record)):
                data_different.append([])
                for j in range (0,len(data_record[i])):
                    data_different[i-1].append(data_record[i][j]-data_record[i-1][j])
            """
            data_different = np.array(data_different,np.float64)
            data_different = data_different.tolist()
            
            record = False
        old_data = data_numpy
        if len(data_back) > 2:
            del data_back[0]
        
        socketio.emit('livedataimu', {'msg': data,'ori': data_ori}, namespace='/web')
        if len(data_different)>0:
            # print(data_different)
            socketio.emit('livedatachange', {'msg': data_different}, namespace='/web')
        #break
        """
        [array([[ 23.38      ,  12.99      ,  28.084     ],                                                      
       [-83.99911451,  25.70183706, 155.72740222],                                                                     
       [-66.35508241,  -4.5820823 , 170.98553051],                                                                     
       [ 35.7890543 ,  27.76963986,  27.22380467],                                                                     
       [  0.        ,   0.        ,   0.        ],                                                                     
       [  0.        ,   0.        ,   0.        ]]), array([[ 23.965     ,  13.01      ,  27.467     ],  
       [-83.91589124,  24.4991844 , 156.05681011],                                                       
       [-65.0677089 ,  -7.70462221, 173.92434743],                                                       
       [ 54.01774816,  62.20516642,  38.88790801],                                                       
       [  0.        ,   0.        ,   0.        ],                                                       
       [  0.        ,   0.        ,   0.        ]]), array([[ 23.11      ,  12.256     ,  26.977     ],  
       [-83.81579283,  25.30011393, 156.66581788],                                                       
       [-63.93555816,  -6.8355401 , 173.73233301],                                                       
       [ 39.30685128,  41.3812273 ,  35.35754568],                                                       
       [  0.        ,   0.        ,   0.        ],                                                       
       [  0.        ,   0.        ,   0.        ]])]    

        """
        # Prepare for the next iteration
        # print(getpid(), "==================DELAY %f ==================" %   samplePeriod)
        time.sleep(samplePeriod)


def background_write_all(data):
    display.write_all([header, ','.join(str(round(i)) for i in data[:3]),
               ','.join(str(round(i))
                        for i in data[3:6]) if inputSize > 3 else '---',
               ','.join(str(round(i)) for i in data[6:9]) if inputSize > 6 else '---', "Good Luck"])


def callback_predict(gt, *args, **kwargs):
    """ Callback for prediction """
    result, time_send = gt.wait()
    if result[0] != 5:
        print(getpid(), time_send, result)


def callback_load_model(gt, *args, **kwargs):
    global model_isloaded
    """ Callback for model loading """
    print(getpid(), "Model is loaded !!")
    model_isloaded = True


# _____________________________ MAIN ____________________________

def main():
    
    # Init IMU MUX
    global display,imu_mux
    mux_channels = [main_mux_channel,7, 6, 5]
    for i in mux_channels:
        try:
            SW.channel(i)
            print(getpid(), "Init IMU #", i)
            imu_mux.append(IMU(i))
        except OSError:
            mux_channels.append(i)
            print(getpid(), "Error Init Channel #", i)
            
    thread_input = eventlet.spawn_n(loop_input)

    # Load keras model
    global model
    if enableML:
        model.load()
        print(model.predictTest())

    print(getpid(), 'RUNNING')
    socketio.run(app, host='0.0.0.0', port='3000')


if __name__ == '__main__':
    main()
