from numpy import genfromtxt
import numpy as np
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras import optimizers
from keras.utils import to_categorical
from keras.models import model_from_json


class Model():
    def __init__(self):
        self.path_json = '../predict/model_imu.json'
        self.path_h5 = '../predict/model_imu_weight.h5'
        #self.path = 'model.h5'
        self.my_model = None

    def load(self):
        print("Loading Model...")
        json_file = open(self.path_json, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.my_model = model_from_json(loaded_model_json)
        self.my_model.load_weights(self.path_h5)
        return True

    def predictFlex(self, data_test, time_send):
        data_test = np.asarray(data_test, dtype="float64")
        output = self.my_model.predict_classes(data_test)
        return output, time_send

    def predictImu(self, data_test, time_send):
        data_test = np.asarray(data_test, dtype="float64")
        output = self.my_model.predict_classes(data_test)
        return output, time_send

    """
    def predictTest(self):
        self.layer()
        data_test = [[[22, 22, 6, 292, 142], [22, 22, 6, 293, 142], [22, 22, 6, 294, 142], [20, 20, 5, 292, 141], [20, 20, 5, 294, 140], [20, 20, 4, 294, 140], [20, 20, 4, 294, 140], [22, 22, 7, 295, 142], [21, 21, 6, 293, 141], [21, 21, 6, 292, 141], [
            21, 21, 6, 292, 141], [20, 21, 5, 291, 140], [20, 21, 5, 291, 140], [20, 21, 5, 291, 140], [20, 20, 5, 291, 140], [21, 22, 6, 290, 139], [21, 21, 5, 291, 139], [20, 21, 5, 291, 139], [20, 21, 5, 291, 139], [20, 20, 5, 292, 139]]]
        data_test = np.asarray(data_test, dtype="float64")
        output = self.my_model.predict_classes(data_test)
        return output
    """

    def predictTest(self):
        self.layer()
        data_test = [[
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1]
        ]]
        data_test = np.asarray(data_test, dtype="float64")
        output = self.my_model.predict_classes(data_test)
        return output

    def layer(self):
        print(self.my_model.summary())
