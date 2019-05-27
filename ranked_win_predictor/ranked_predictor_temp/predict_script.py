# MLP for ranked predtcitor deserialize from JSON and HDF5
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from sklearn.preprocessing import MinMaxScaler
from numpy import array
from pandas import DataFrame
import numpy
import os
from .get_live_game import get_live_game

#choose summoner in game
summoner = input('enter summoner name: ')
#get data from game
df = DataFrame(get_live_game(summoner))
Xnew = df.to_numpy()
# load json and create model
json_file = open('ranked_predictor_temp\model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("ranked_predictor_temp\model.h5")
print("Loaded model from disk")
# make a prediction
ynew = loaded_model.predict_classes(Xnew)
# show the inputs and predicted outputs
print('1 = blue side win 0 = red side win\n')
print("X=%s, Predicted=%s" % (Xnew[0], ynew[0]))
    