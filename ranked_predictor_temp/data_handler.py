import numpy
import pandas as pd

API_KEY = '?api_key=RGAPI-d46343f5-bcf7-461a-a1bf-a00d7c16ac80'
BASE_URL = 'https://euw1.api.riotgames.com/lol/'
BASE_URL_CHAMPIONGG = 'http://api.champion.gg/v2/champions/'
SUMMONER_BY_NAME = 'summoner/v4/summoners/by-name/'
MATCHLIST_BY_ACCOUNT = 'match/v4/matchlists/by-account/'
MATCH_BY_MATCHID = 'match/v4/matches/'

class DataHandler:
    #construct datahandler object with player using tool and their current game
    def __init__(self, gameId):
        self.gameId = gameId
    #get average winrate of all players for a team
    def get_avg_winrate(self):
        percentage_wr = 50
        if self.gameId == 'hello':
            percentage_wr = 544
        return percentage_wr
    #get average champion mastery of all players of a team
    def get_avg_champion_mastery(self):
        avg_mastery = 50000
        return avg_mastery
    #get average champion winrate for a team
    def get_avg_champion_winrate(self):
        avg_winrate = 53
        return avg_winrate

    def get_winstreak_total(self):
        winstreak_total = -3
        return winstreak_total

def generate_modelled_data(gameId):
    return None

dh = DataHandler('helo')
x = dh.get_avg_winrate()
print(x)