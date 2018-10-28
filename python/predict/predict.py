from sklearn.neural_network import MLPClassifier
from numpy import genfromtxt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib

scalerFlex = StandardScaler()
scalerImu = StandardScaler()
mlp_flex = joblib.load('../predict/model.joblib')
mlp_imu = joblib.load('../predict/model_imu.joblib')


def setScalarFlex():
    training_data = genfromtxt('../predict/export_to_num.csv', delimiter=',')
    X = training_data[:525:, 0:5]
    y = training_data[:525, 5]
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    scalerFlex.fit(X_train)


def setScalarImu():
    training_data = genfromtxt('../predict/export_imu.csv', delimiter=',')
    X = training_data[:, 0:9]
    y = training_data[:, 9]
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    scalerImu.fit(X_train)


def predictFlex(data_test):
    data_test = np.asarray(data_test, dtype="float64")
    data_test = scalerFlex.transform(data_test)
    output = mlp_flex.predict(data_test)
    return output


def predictImu(data_test):
    data_test = np.asarray(data_test, dtype="float64")
    data_test = scalerImu.transform(data_test)
    output = mlp_imu.predict(data_test)
    return output


def predictAll(data_test):
    data_test1 = np.asarray([data_test[9:]], dtype="float64")
    data_test1 = scalerFlex.transform(data_test1)
    output1 = mlp_flex.predict(data_test1)

    data_test2 = np.asarray([data_test[:9]], dtype="float64")
    data_test2 = scalerImu.transform(data_test2)
    output2 = mlp_imu.predict(data_test2)
    return [output1, output2]


setScalarFlex()
setScalarImu()
