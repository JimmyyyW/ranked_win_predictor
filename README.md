# ranked_win_predictor
University project. Using a neural net to predict likelihood of winning upon entering game of league of legends

ALWAYS REGENERATE API KEYS BEFORE ATTEMPTING TO RUN ANY PROGRAMS

"python.jediEnabled": false in python settings.json may cause import issues.

## DATA COLLECTION
If running the project from scratch, first you must run the collect.py file using the following console command, or being
ran from an IDE. Whenprompted to input a summoner name, please use your own summoner name (IGN) and if you don't have one and are using the 
project for none-LoL related purposes, go to [https://euw.op.gg/ranking/ladder/ and take one].

```
    python collect.py
```

It is recommended to collect 20000 data points using that one summoner name. This is prompted in the script. 

NOTE: IF THIS ERRORS, CHECK API KEY, this is a failsafe as to not send invalid requests to the riot games api

## TRAIN THE NEURAL NET
providing you have data collected (my training consisted of around 14k samples) the training should be ready to go ahead. Various settings can be changed withing neural_model.py. The current settings have been configured through iterative testing. To train the model, run the following command. THIS WILL OVERWRITE THE SAVED WEIGHTS (unless you change the filepath)

```
    python neural_model.py
```

## USE THE MODEL TO PREDICT
Run predict.py, enter a summoner name of a summoner who is currently in a live game and you will receive a predicted value (1 or 0) for win or loss respectively.

```
    python predict_sript.py
```
