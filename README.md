# ranked_win_predictor
University project. Using a neural net to predict likelihood of winning upon entering game of league of legends

"python.jediEnabled": false in python settings.json may cause import issues.

DATA COLLECTION
If running the project from scratch, first you must run the collect.py file using the following console command, or being
ran from an IDE. Whenprompted to input a summoner name, please use your own summoner name (IGN) and if you don't have one and are using the 
project for none-LoL related purposes, go to https://euw.op.gg/ranking/ladder/ and take one. 
"""
    python {path}collect.py
"""
By default the program is set to take 40000 data points using that one summoner name. This can be set using the 'thresh' parameter in match_crawler
in the 'crawler_writer' function. This generally runs at around 

DATA MODELLING
The next step is to model the data you have collected this is performed by runnning the model.py file using the following console
command, or being ran from an IDE. This is the longest part of the process as for each input node of the nueral network model a number of
api calls must be performed to get the necessary data, as well as some computing to normalise the data.
"""
    python model.py
"""

TRAINING AND TESTING THE MODEL

"""
    neural model.py
"""