# Import standard libs
import sys
import time
import datetime
import random
import json
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
from oled import init_oled, write_all, write_row

# Import ML modules
sys.path.insert(0, '../predict')
from predict import Model

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
threshold = [25 for i in range(inputSize)]
# MUX Channels
imu_mux = []
# KERAS MODEL
model = Model()
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

# _____________________________ Flask __________________________________


@app.route('/')
@app.route('/api')
def index():
    return "Hello World"


@app.route('/predict/all')
def predict_all_handler():
    data = request.args.get('data')
    data = [int(i) for i in json.loads(data)]
    # print(getpid(),data)
    # thread_predict = eventlet.spawn(
    #     background_predictAll, data)
    # thread_predict.link(callback_predict)
    return ":)"


@app.route('/predict/moveflex')
def predict_moveflex_handler():
    global model, model_isloaded
    if model_isloaded:
        data = request.args.get('data')
        data = [[int(i) for i in j[9:]] for j in json.loads(data)]
        time_send = request.args.get('time')
        # print(getpid(), data)
        thread_predict = eventlet.spawn(model.predictFlex, [data], time_send)
        thread_predict.link(callback_predict)
        return ":)"
    else:
        return ":("


@app.route('/predict/moveimu')
def predict_moveimu_handler():
    global model, model_isloaded
    if model_isloaded:
        data = request.args.get('data')
        data = [[int(i) for i in j[:6]] for j in json.loads(data)]
        time_send = request.args.get('time')
        # print(getpid(), data)
        result, time_send = model.predictImu([data], time_send)
        print(getpid(), time_send, result)
        #thread_predict = eventlet.spawn(model.predictImu, [data], time_send)
        # thread_predict.link(callback_predict)
        return str(result[0])
    else:
        return ":("


@app.route('/predict/test')
def predict_test_handler():
    global model, model_isloaded
    if model_isloaded:
        # print(getpid(), data)
        print(model.predictTest())
        # thread_predict.link(callback_predict)
        return ":)"
    else:
        return ":("


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
    eventlet.spawn_n(write_row, text="Starting....")

    start = datetime.datetime.now()
    while True:
        data = [[] for i in imu_mux]
        for i, cur_imu in enumerate(imu_mux):
            # Switch mux channel & Read data
            SW.channel(cur_imu.get_channel())
            data[i] = [round(d, 3) for d in cur_imu.get_all(start)]
            # print(getpid(), "Channel#", cur_imu.get_name(), data[i])

            # # Calculation
            # if len(datas) > windowSize:
            #     eventlet.spawn_n(background_process_accel, data)
            #     datas = datas[1:]
            # datas.append(data)

        # # Export Data through socket/oled
        # thread_oled = eventlet.spawn_n(background_write_all, data)
        # # fill the missing imu
        data = data + [dummy_imu() for i in range(len(data), 6)]
        eventlet.spawn_n(background_livedata, data)

        # Prepare for the next iteration
        #print(getpid(), "==================DELAY %f ==================" %   samplePeriod)
        time.sleep(samplePeriod)
        start = datetime.datetime.now()


def background_livedata(data):
    dataset = data
    socketio.emit('livedata', {'msg': dataset}, namespace='/web')


def background_write_all(data):
    write_all([header, ','.join(str(round(i)) for i in data[:3]),
               ','.join(str(round(i))
                        for i in data[3:6]) if inputSize > 3 else '---',
               ','.join(str(round(i)) for i in data[6:9]) if inputSize > 6 else '---', "Good Luck"])


def background_process_accel(newData):
    global avgData, movingData
    diff = [0 for i in range(inputSize)]
    avgData = [sum(map(lambda d: d[i], datas)) /
               windowSize for i in range(inputSize)]
    diff = [round(newData[i]-avgData[i]) for i in range(inputSize)]
    # print(getpid(),'\t'.join([str(round(x)) for x in avgData]))

    for i in range(inputSize):
        if(abs(diff[i]) > threshold[i]):
            movingData.append(diff)
            break
        elif(i == inputSize-1):
            if len(movingData) > 0:
                avgMoving = [round(sum(map(lambda d: d[i], movingData)) /
                                   len(movingData), 3) for i in range(inputSize)]
                movingData = []
                # thread_predict = eventlet.spawn(background_predict, avgMoving)
                # thread_predict.link(callback_predict)
                eventlet.spawn_n(background_write_all, avgMoving)
                # print(getpid(),"Move:", avgMoving)

    # for i in range(3):
        # if(abs(newData[i]-avgData[i])):


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
    global model
    # Init IMU MUX
    for i in [0, 1, 7]:
        try:
            SW.channel(i)
            print(getpid(), "Init IMU #", i)
            imu_mux.append(IMU(i))
        except OSError:
            print(getpid(), "Error Init Channel #", i)
    thread_input = eventlet.spawn_n(loop_input)

    # Load keras model
    model.load()
    print(model.predictTest())

    print(getpid(), 'RUNNING')
    socketio.run(app, host='0.0.0.0', port='3000')


if __name__ == '__main__':
    main()
