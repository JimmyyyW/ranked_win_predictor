import numpy
import pandas as pd
import time
from match_crawler import get_request

API_KEY = '?api_key=RGAPI-a26d98e8-b93b-4d7b-ad13-c6df50cc7eb3'
BASE_URL = 'https://euw1.api.riotgames.com/lol/'
BASE_URL_CHAMPIONGG = 'http://api.champion.gg/v2/champions/'
SUMMONER_BY_NAME = 'summoner/v4/summoners/by-name/'
MATCHLIST_BY_ACCOUNT = 'match/v4/matchlists/by-account/'
MATCH_BY_MATCHID = 'match/v4/matches/'
LEAGUE_BY_SUMMONER = 'league/v4/entries/by-summoner/'


class DataHandler:
    #construct datahandler object with player using tool and their current game
    def __init__(self, gameId_input):
        self.gameId = gameId_input

    #get all players from game
    def get_summonerIds_from_game(self):
        summonerIds = {}
        i=0
        match_data = get_request(BASE_URL+MATCH_BY_MATCHID+self.gameId)
        for data in match_data:
            data = (match_data['participantIdentities'])
            for player in data:
                while i<10:
                    player = data[i]
                    i=i+1
                    summoner = (player['player'])
                    summonerIds[player['participantId']]=(summoner['summonerId'])
        return summonerIds

    def get_ranked5x5_by_summoner(self, summonerIds):
        i=1
        ranked_stats = []
        print('collecting summoner data...')
        for summonerId in summonerIds:
            while i < 11:
                summonerId = summonerIds.get(i)
                i+=1
                summoner_league_data = get_request(BASE_URL+LEAGUE_BY_SUMMONER+summonerId)
                time.sleep(0.5)
                if len(summoner_league_data) == 3:
                    ranked_5x5 = summoner_league_data[2]
                if len(summoner_league_data) == 2:
                    ranked_5x5 = summoner_league_data[1]
                else:
                    ranked_5x5 = summoner_league_data[0]
                ranked_stats.append(ranked_5x5)
        return ranked_stats

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

dh = DataHandler('4019902021')
test = dh.get_ranked5x5_by_summoner(dh.get_summonerIds_from_game())
print(test)
