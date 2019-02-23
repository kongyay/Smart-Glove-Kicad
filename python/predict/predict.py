import numpy as np
from numpy import genfromtxt
from sklearn.preprocessing import StandardScaler

class Model():
    def __init__(self):
        self.path_json = '../predict/model_imu.json'
        self.path_h5 = '../predict/model_imu_weight.h5'
        self.path_csv = '../predict/raw_data.csv'
        #self.path = 'model.h5'
        self.my_model = None
        self.scalar = StandardScaler()

    def load(self):
        from keras.models import model_from_json
        print("Loading Model...")
        json_file = open(self.path_json, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.my_model = model_from_json(loaded_model_json)
        self.my_model.load_weights(self.path_h5)
        training_data = genfromtxt(self.path_csv, delimiter=',')
        data_normalize = training_data[:,0:36]
        self.scalar.fit(data_normalize)
        return True

    def predictFlex(self, data_test):
        data_test = np.asarray(data_test, dtype="float64")
        output = self.my_model.predict_classes(data_test)
        return output

    def predictImu(self, data_test, poses_pool, max_pose):
        math = []
        max_train = 17
        for i in range (max_train):
            if i in poses_pool:
                math.append(1)
            else:
                math.append(0)    
        data_test = self.scalar.transform(data_test)
        data_test = [data_test]
        data_test = np.asarray(data_test, dtype="float64")
        prob = self.my_model.predict(data_test)
        prob = np.multiply(prob, math)
        output = np.argmax(prob)
        return output

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
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
        ]]
        data_test = np.asarray(data_test, dtype="float64")
        output = self.my_model.predict_classes(data_test)
        return output

    def layer(self):
        print(self.my_model.summary())

class NullModel():
    def __init__(self):
        return

    def load(self):
        return

    def predictFlex(self, data_test):
        return [1]

    def predictImu(self, data_test):
        return [1]

    def predictTest(self):
        return [1]

        