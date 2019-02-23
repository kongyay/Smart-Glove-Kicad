# Import standard libs
import sys
import time
from datetime import datetime
import random
import json
import numpy as np
from os import system

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
from imu import IMU,NullIMU
from mux import SW
from oled import display
 
# Import ML modules 
enableML = True
sys.path.insert(0, '../predict')
if enableML:
    from predict import Model 
    model = Model()
else:
    print("=== NOT USING TENSORFLOW ===")
    from predict import NullModel
    model = NullModel()

# Import DB libs
from models import Gesture, Pose, GestureAction, Action, Profile

# Import NW/Action
from network import nw
from action import actionMaker

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
imu_ok = [False,False,False,False,False,False]
# Last prediction
last_poses = []
stack_poses = []
# Boolean if model is loaded
model_isloaded = True
# Current Profile
cur_profile = "Default"
poses_pool = []
# Size of sample/second
sampleRate = 10

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
def on_predict(data,add=True):
    global last_poses,stack_poses, model, poses_pool
    print("Predicting...")
    if len(data)<sampleRate:
        return
    data = [x[0]+x[1]+x[2]+x[3]+x[4]+x[5] if(len(x)==6) else x for x in data]
    result = model.predictImu(data,poses_pool,len(Pose.objects))
    result = Pose.objects(index = int(result)).first().name
    # # If same pose, ignore...
    #if (result not in poses_pool) or (len(last_poses)>0 and result == last_poses[-1]):
        #return
    print("Pose:",result)
    last_poses.append(result)
    if add:
        stack_poses.append(result)
    display.write_row(text="Pos: "+">".join(stack_poses[-5:]),row=1)
    
    ga = checkGesture()
    if ga:
        display.write_row(text='Ges: ' + ga.gesture.name,row=2)
        actionMaker.do(type=ga['action']['name'],args=ga['args'])
    else:
        display.write_row(text='Ges: None',row=2)
    socketio.emit('predict_result', result, namespace='/web')

@socketio.on('profiles', namespace='/web')
def on_profile():
    print("Fetch Profiles!")
    socketio.emit('profiles_result',[cur_profile]+[i.to_json() for i in Profile.objects],namespace='/web')

@socketio.on('choices', namespace='/web')
def on_profile():
    print("Fetch All Pose!")
    socketio.emit('choices_result',[[i.to_json() for i in Pose.objects],[i.to_json() for i in Action.objects],[i.to_json() for i in Gesture.objects]],namespace='/web')

@socketio.on('saveGA', namespace='/web')
def on_saveGA(profile_name,old_name,data):
    print("Save GA Request!",profile_name)
    profile = Profile.objects(name=profile_name).first()
    gesture = Gesture.objects(name=data['gesture']['name']).first()
    action = Action.objects(name=data['action']['name']).first()
    for i in range(len(profile.gestures_actions)):
        if old_name == profile.gestures_actions[i].gesture.name:
            profile.gestures_actions[i].gesture = gesture
            profile.gestures_actions[i].action = action
            profile.gestures_actions[i].args = data['args']
            # print(profile.gestures_actions[i].args,data['args'])
            profile.save()
            socketio.emit('notify','SAVED',namespace='/web')
            return

    print("New GA!")
    profile.gestures_actions.append(GestureAction(gesture=gesture,action=action,args=data['args']))
    profile.save()
    socketio.emit('notify','NEW',namespace='/web')

@socketio.on('removeGA', namespace='/web')
def on_removeGA(profile_name,name):
    print("Remove GA Request!",name)
    profile = Profile.objects(name=profile_name).first()
    for i in range(len(profile.gestures_actions)):
        if name == profile.gestures_actions[i].gesture.name:
            del profile.gestures_actions[i]
            profile.save()
            socketio.emit('notify','REMOVED',namespace='/web')
            return

    print("Remove GA Error!")
    socketio.emit('notify','REMOVE ERROR',namespace='/web')
    

@socketio.on('saveGesture', namespace='/web')
def on_saveGesture(data):
    print("Save Gesture Request!",data)

    gestures = Gesture.objects(name=data['name'])
    if(len(gestures)>0):
        gesture = gestures.first()
        poses = []
        for np in data['poses']:
            poses.append(Pose.objects(name=np['name']).first())
            
        gesture.poses = poses
        gesture.save()
        socketio.emit('notify','SAVED',namespace='/web')
        return

    print("New Gesture!")
    poses = []
    for np in data['poses']:
        poses.append(Pose.objects(name=np['name']).first())
    gesture = Gesture(name=data['name'],poses=poses)
    gesture.save()
    socketio.emit('notify','NEW',namespace='/web')

@socketio.on('removeGesture', namespace='/web')
def on_removeGesture(data):
    print("Remove Gesture Request!",data)
    
    gestures = Gesture.objects(name=data)
    if(len(gestures)>0):
        gestures.first().delete()
        socketio.emit('notify','SUCCESS',namespace='/web')  
    else:
        print("Gesture not found!")
        socketio.emit('notify','FAIL',namespace='/web')  

@socketio.on('createProfile', namespace='/web')
def on_createProfile(profile_name):
    print("Create profile Request!",profile_name)
    
    profile = Profile(name=profile_name)
    profile.save()
    socketio.emit('notify','Created',namespace='/web')

@socketio.on('removeProfile', namespace='/web')
def on_removeProfile(profile_name):
    global cur_profile
    print("Remove profile Request!",profile_name)
    profile = Profile.objects(name=profile_name)
    if(len(profile)>0):
        profile.first().delete()
        cur_profile = 'Default'
        socketio.emit('notify','Removed',namespace='/web')  
    else:
        print("Profile not found!")
        socketio.emit('notify','Remove fail',namespace='/web')  

@socketio.on('switchProfile', namespace='/web')
def on_switchProfile(profile_name):
    global cur_profile,poses_pool
    print("Switch Profile to",profile_name)
    cur_profile = profile_name
    poses_pool = set([])
    pf = Profile.objects(name=profile_name).first()
    for ga in pf['gestures_actions']:
        for p in ga['gesture']['poses']:
            poses_pool.add(p['index'])
    print('New pose pool:',poses_pool)

@socketio.on('openAP', namespace='/web')
def on_changeNwMode():
    print("Change NW to AP")
    nw.switch_con('g2g','')

@socketio.on('switchNw', namespace='/web')
def on_switchNw(name,pw):
    print("Switch NW to",name,pw)
    nw.switch_con(name,pw)

@socketio.on('getNw', namespace='/web')
def on_scanNw():
    print("Getting NW...")
    socketio.emit('get_nw_result',nw.get_cons(),namespace='/web')  

@socketio.on('setTime', namespace='/web')
def on_setTime(time):
    print("Setting Time...",time)
    system('date -s %s' % time)
    display.show_clock()
    socketio.emit('notify',"Date,Time changed!",namespace='/web')  
    
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
    # gesture2 = Gesture(name="OpenClose", poses=[pose2,pose1])
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
    global stack_poses,cur_profile
    profile = Profile.objects(name=cur_profile).first()
    re_l = stack_poses[::-1]
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
            stack_poses = [] # Flush history
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

# _____________________________ THREAD/LOOP/BG ____________________________


def loop_input():
    print("Starting input loop...")
    
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
    rotate_threshold = 10
    # Minimum number of same data in sequence that considered as idle
    idle_min = 20
    # Counter for idle_min
    idle_count = 0
    # Lap for each moving predict
    moving_lap = 3
    # Counter for moving_lap
    moving_count = 0
    # Flag to check for each finger to move
    idle_flags = [True for i in imu_mux]
    # Flag to check if idle pose changed
    pose_flag = False
    

    record = False
    first = True

    while True:
        data = [[] for i in imu_mux]
        data_ori = [[] for i in imu_mux]
        starttime = [datetime.now() for i in imu_mux]
        for i, cur_imu in enumerate(imu_mux):
            # Switch mux channel & Read data
            try:
                SW.channel(cur_imu.get_channel())
            except (Exception):
                data[i] = dummy_accgyro()
                # print("Switch channel fail #", cur_imu.get_channel())

            data[i],starttime[i] = cur_imu.get_all(starttime[i])
            data[i] = [round(data[i][j],6) for j in range(6)]
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
            if len(datas) > 0:
                if all(abs(data[i][j]-datas[-1][i][j]) < rotate_threshold for j in range(3,6)):
                    data[i] = datas[-1][i]
                    idle_flags[i] = True
                else:
                    # # if not all axes in a finger in idle, set idle = False
                    idle_flags[i] = False

            # print("Channel#", cur_imu.get_name(), data[i])

        ## ======================= END OF ALL FINGER =======================================

        # # fill the missing imu
        data = data + [dummy_accgyro() for i in range(len(data), 6)]

        # # Check for changes
        if not all(idle_flags):
            # # Moving
            moving_count += 1
            if moving_count % moving_lap == 0:
                # on_predict(datas,add=False)
                moving_count = 3
                idle_count = 0
        else:
            # # if idle
            if idle_count == 0:
                on_predict(datas)
                print(".......Idle......")
            if idle_count < 5:
                idle_count += 1
                # on_predict(datas,add=False)
    
        # # Keep data_back in size of sampleRate
        if len(datas) >= sampleRate:
            datas = datas[1:]
        datas.append(data)
        # print(data[i])
        socketio.emit('live_imu', {'msg': data,'ori': data_ori}, namespace='/web')
        


        # Prepare for the next iteration
        # print("================== DELAY %f ==================" %   samplePeriod)
        time.sleep(samplePeriod)

def loop_ipcheck():
    while True:
        old_ip = str(nw.ip)
        new_ip = str(nw.get_ip())
        if old_ip != new_ip:
            display.set_info("ip",new_ip)
            display.show_clock()
        time.sleep(10)

def loop_clockcheck():
    while True:
        display.set_info("dt",datetime.now())
        display.show_clock()
        time.sleep(60) 

def callback_load_model(gt, *args, **kwargs):
    global model_isloaded
    """ Callback for model loading """
    print("Model is loaded !!")
    model_isloaded = True 


# _____________________________ MAIN ____________________________

def main():
    
    # Init IMU MUX
    global display,imu_mux,actionMaker
    mux_channels = [main_mux_channel, 3,4,5,6,7]
    for i,channel in enumerate(mux_channels):
        try:
            SW.channel(channel)
            print("Init IMU #", channel)
            imu_mux.append(IMU(channel,i))
        except OSError as e:
            # # Retry init 
            # mux_channels.append(channel)
            imu_mux.append(NullIMU(channel,i))
            print("Error Init Channel #", channel,e)
            
    thread_input = eventlet.spawn_n(loop_input)

    # Init Check loop
    thread_ipchange = eventlet.spawn_n(loop_ipcheck)
    thread_clockchange = eventlet.spawn_n(loop_clockcheck)

    # Load keras model
    global model
    model.load()
    print(model.predictTest())

    # Set action display
    actionMaker.setDisplay(display)
    on_switchProfile('Default')

    print('RUNNING')
    socketio.run(app, host='0.0.0.0', port='3000')


if __name__ == '__main__':
    main()
