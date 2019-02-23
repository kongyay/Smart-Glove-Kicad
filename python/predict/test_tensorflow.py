from keras.models import Sequential
from keras.layers import Dense
from numpy import genfromtxt
import numpy
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# fix random seed for reproducibility
numpy.random.seed(7)
# load pima indians dataset
training_data = genfromtxt('export_to_num.csv', delimiter=',')
# split into input (X) and output (Y) variables
X = training_data[:946:,0:5]
y = training_data[:946,5]
X_train, X_test, y_train, y_test = train_test_split(X, y)

model = Sequential()
model.add(Dense(64, input_dim=5, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])
# Fit the model
model.fit(X_train, y_train, epochs=150)
# evaluate the model
scores = model.evaluate(X_train, y_train)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
