import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import Perceptron
iris = load_iris()
print(iris.data[:3])
print(iris.data[15:18])
print(iris.data[37:40])
# we extract only the lengths and widthes of the petals:
X = iris.data[:, (2, 3)]   
