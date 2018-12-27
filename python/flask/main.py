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
sys.path.insert(0, '../predict')
if enableML:
    from predict import Model
    model = Model()
else:
    from predict import NullModel
    model = NullModel()

# Import DB libs
from models import Gesture, Pose, GestureAction, Action, Profile

# Import NW
from network import nw

# VARIABLES
# smallest possible difference
EPSILON = sys.float_info.epsilon
# Connected Socket Clients
connectedClients = 0
# OLED Header
header = '-([Glove 2 Gesture])-'

# MUX Channels
imu_mux = []
main_mux_channel = 1

# Last prediction
last_poses = []

# Boolean if model is loaded
model_isloaded = True

# _____________________________ SOCKET.IO Handlers __________________________________


@socketio.on('connect', namespace='/web')
def on_connect():
    global connectedClients
    connectedClients += 1
    print('Client Connected')


@socketio.on('disconnect', namespace='/web')
def on_disconnect():
    global connectedClients
    connectedClients -= 1
    print('Client Disconnected')


@socketio.on('ping', namespace='/web')
def on_ping():
    print("GOT PING :D :) :P ==========")
    socketio.emit('pong', 'This is pong :)', namespace='/web')


@socketio.on('resample', namespace='/web')
def on_resample(gestures, size):
    print("Resampling...", size)
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
    global last_poses, model
    result = model.predictImu([data], None)    
    result = Pose.objects()[result[0]-1].name
    print("Pose:",result)
    last_poses.append(result)
    display.write_row(text="Pos: "+">".join(last_poses),row=1)
    
    ga = checkGesture()
    if ga:
        display.write_row(text='Ges: '+ga.gesture.name,row=2)
    else:
        display.write_row(text='Ges: None',row=2)
    socketio.emit('predict_result', result, namespace='/web')

@socketio.on('profiles', namespace='/web')
def on_profile():
    print("Fetch Profiles!")
    socketio.emit('profiles_result',[i.to_json() for i in Profile.objects],namespace='/web')

@socketio.on('choices', namespace='/web')
def on_profile():
    print("Fetch All Pose!")
    socketio.emit('choices_result',[[i.to_json() for i in Pose.objects],[i.to_json() for i in Action.objects],[i.to_json() for i in Gesture.objects]],namespace='/web')

@socketio.on('saveGesture', namespace='/web')
def on_saveGesture(profile_name,data):
    print("Save Gesture Request!",profile_name,data)
    profile = Profile.objects(name=profile_name).first()
    for i in range(len(profile.gestures_actions)):
        if data['gesture']['name'] == profile.gestures_actions[i].gesture.name:
            gesture = Gesture.objects(name=data['gesture']['name']).first()
            poses = []
            for np in data['gesture']['poses']:
                poses.append(Pose.objects(name=np['name']).first())
                
            gesture.poses = poses
            gesture.save()
            profile.gestures_actions[i].action = Action.objects(name=data['action']['name']).first()
            profile.gestures_actions[i].args = data['args']
            profile.save()
            socketio.emit('save_gesture_result','SAVED',namespace='/web')
            return

    print("New Gesture!")
    poses = []
    for np in data['gesture']['poses']:
        poses.append(Pose.objects(name=np['name']).first())
    gesture = Gesture(name=data['gesture']['name'],poses=poses)
    gesture.save()
    action = Action.objects(name=data['action']['name']).first()
    profile.gestures_actions.append(GestureAction(gesture=gesture,action=action,args=data['args']))
    profile.save()
    socketio.emit('save_gesture_result','NEW',namespace='/web')

@socketio.on('removeGesture', namespace='/web')
def on_removeGesture(profile_name,data):
    print("Remove Gesture Request!",profile_name,data)
    profile = Profile.objects(name=profile_name).first()
    for i in range(len(profile.gestures_actions)):
        if data['gesture']['name'] == profile.gestures_actions[i].gesture.name:
            gesture = Gesture.objects(name=data['gesture']['name']).first()
            gesture.delete()
            
            socketio.emit('remove_gesture_result','OK',namespace='/web')
            return
    print("Gesture not found!")
    socketio.emit('save_gesture_result','FAIL',namespace='/web')  

@socketio.on('openAP', namespace='/web')
def on_changeNwMode():
    print("Change NW to AP")
    nw.switch_con('g2g')

@socketio.on('switchNw', namespace='/web')
def on_switchNw(name,pw):
    print("Switch NW to",name,pw)
    nw.switch_con(name,pw)

@socketio.on('getNw', namespace='/web')
def on_scanNw():
    print("Getting NW...")
    socketio.emit('get_nw_result',nw.get_cons(),namespace='/web')  
# _____________________________ Flask __________________________________

@app.route('/')
@app.route('/api')
def index():
    return "Hello World"

@app.route('/profiles')
def get_gestures():
    print("Get Profiles!")
    pose_col = Pose._get_collection()
    ges_col = Gesture._get_collection()


    # pose1 = Pose.objects(name='Close').first()
    # pose2 = Pose.objects(name='Open').first()
    # gesture1 = Gesture(name="CloseOpen", poses=[pose1,pose2])
    # print(getpid(),gesture1)
    # gesture2 = Gesture(name="OpenClose", poses=[pose2,pose1])
    # print(getpid(),gesture2)
    # gesture1.save()
    # gesture2.save()

    # gesture = Gesture.objects(name="CloseOpen").first()
    # action = Action.objects(name='Display').first()
    # profile = Profile(name='Default')
    # profile.gestures_actions = [GestureAction(gesture=gesture,action=action,args=['GumBear'])]
    # profile.save()

    return str([i.to_json() for i in Profile.objects]) 

# _____________________________ Functions __________________________________

def checkGesture():
    global last_poses
    profile = Profile.objects(name='Default').first()
    re_l = last_poses[::-1]
    for ga in profile.gestures_actions: # For each gesture
        re_p = ga.gesture.poses[::-1]
        ## If a number of last poses less than this gesture's pose, skip this gesture
        if(len(re_l)<len(re_p)):
            continue
        ## Poses Comparison
        match = True
        for i in range(len(re_p)): # For each pose
            # print(re_p[i].name,re_l)
            if re_p[i].name == re_l[i]:
                continue
            else:
                match = False
                break
        ## If match all pose = FOUND MATCHED GESTURE
        if match == True:
            last_poses = [] # Flush history
            return ga

    return None
        
        

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
    print("Starting input loop...")
    
    # Size of sample/second
    sampleRate = 20
    # Period of capturing each sample
    samplePeriod = 1.0/sampleRate
    # Input size 3:Ac, 6:AcGy, 9:AGM, 12:AGMF
    inputSize = 6
    # Sliding data
    datas = []
    # Last idle data
    data_last_idle = []
    # Moving data since start moving to stop moving
    datas_moving = []
    # Threshold which one of each value considered as start moving
    moving_threshold = 30
    # Minimum number of same data in sequence that considered as idle
    idle_min = 20
    # Counter for idle_min
    idle_count = 0
    # Flag to check for each finger to move
    idle_flags = [True for i in imu_mux]
    # Flag to check if idle pose changed
    pose_flag = False
    

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
            except (Exception):
                data[i] = dummy_imu()
                print("Switch channel fail #", cur_imu.get_channel())

            data[i],starttime[i] = cur_imu.get_all(starttime[i])
            data[i] = [round(data[i][j],3) for j in range(3)]
            data_ori[i] = data[i][:]



            # find differences between fingers and center
            # if(i != 0):
            #     bound = [30,90,30]
            #     diff_data = data[:]
            #     for j in range(3):
            #         diff_data[i][j] = angle_diff(data[i][j], data[0][j])
            #         if diff_data[i][j] > bound[j] or diff_data[i][j] < -bound[j]:
            #             if data[i][j] > data[0][j]:
            #                 data[i][j] = 100
            #             else:
            #                 data[i][j] = -100
            #         else:
            #             data[i][j] = 0
                    # if diff_data[i][j] > bound[j] or diff_data[i][j] < -bound[j]:
                    #     data[i][j] = 200
                    # elif diff_data[i][j] > bound[j]/2 or diff_data[i][j] < -bound[j]/2:
                    #     data[i][j] = 100
                    # else:
                    #     data[i][j] = 0


            # # Smooth out
            # if len(datas) > 0:
            #     if all(abs(angle_diff(data[i][j],datas[-1][i][j])) < moving_threshold for j in range(3)):
            #         data[i] = datas[-1][i]
            #         idle_flags[i] = True
            #     else:
            #         # # if not all axes in a finger in idle, set idle = False
            #         idle_flags[i] = False

            #print("Channel#", cur_imu.get_name(), data[i])

        # # Export Data through socket/oled
        # # fill the missing imu
        data = data + [dummy_imu() for i in range(len(data), 6)]

        # # Check for changes
        if not all(idle_flags):
            datas_moving.append(data)
            socketio.emit('live_imu', {'msg': data,'ori': data_ori,'idle':False}, namespace='/web')
            pose_flag = True
        else:
            # # if idle
            datas_moving = []
            idle_count += 1
            # # if pose changed
            socketio.emit('live_imu', {'msg': data,'ori': data_ori,'idle':False}, namespace='/web')
            if pose_flag and idle_count >= idle_min:
                socketio.emit('live_imu', {'msg': data,'ori': data_ori,'idle':True}, namespace='/web')
                data_last_idle = data
                pose_flag = False
                idle_count = 0

        # # Keep data_back in size of sampleRate
        if len(datas) > sampleRate:
            datas = datas[1:]
        datas.append(data)

        # socketio.emit('live_imu', {'msg': data,'ori': data_ori}, namespace='/web')
        

        # Prepare for the next iteration
        # print("==================DELAY %f ==================" %   samplePeriod)
        time.sleep(samplePeriod)

def loop_ipcheck():
    while True:
        old_ip = str(nw.ip)
        new_ip = str(nw.get_ip())
        disp_text = "IP: " + new_ip + ('*' if old_ip != new_ip else '')
        display.write_row(text=(disp_text))
        time.sleep(10)

def callback_load_model(gt, *args, **kwargs):
    global model_isloaded
    """ Callback for model loading """
    print("Model is loaded !!")
    model_isloaded = True 


# _____________________________ MAIN ____________________________

def main():
    
    # Init IMU MUX
    global display,imu_mux
    mux_channels = [main_mux_channel,7, 6, 5, 4, 3]
    for i,channel in enumerate(mux_channels):
        try:
            SW.channel(channel)
            print("Init IMU #", channel)
            imu_mux.append(IMU(channel,i))
        except OSError:
            mux_channels.append(channel)
            print("Error Init Channel #", channel)
            
    thread_input = eventlet.spawn_n(loop_input)

    # Init Network
    thread_ipchange = eventlet.spawn_n(loop_ipcheck)

    # Load keras model
    global model
    model.load()
    print(model.predictTest())

    print('RUNNING')
    socketio.run(app, host='0.0.0.0', port='3000')


if __name__ == '__main__':
    main()
