from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import keras
import numpy

# random seed for reproducibility
numpy.random.seed(2)

# loading load game dataset, one data entry = one game
dataset = numpy.loadtxt("game_data.csv", delimiter=",")

#create scalar
scaler = MinMaxScaler()

#fit scaler on Data
scaler.fit(dataset)

#transform data
normalised = scaler.transform(dataset)

# split into input (X) and output (Y) variables, splitting csv data
X = normalised[:,1:5]
Y = normalised[:,5]

# split X, Y into a train and test set
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.20, random_state=42)

# create model, add dense layers one by one specifying activation function
model = Sequential()
model.add(Dense(256, input_dim=4, activation='relu')) # input layer requires input_dim param
#model.add(Dropout(.2))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
#model.add(Dropout(.2))
model.add(Dense(1, activation='sigmoid')) # sigmoid instead of relu for final probability between 0 and 1

# compile the model, adam gradient descent (optimized)
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])

# call the function to fit to the data (training the network)
model.fit(x_train, y_train, epochs = 700, batch_size=20, validation_data=(x_test, y_test))

#calculate predictions
predictions = model.predict(X)

#evaluate model
scores = model.evaluate(X,Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")
 
# later...
