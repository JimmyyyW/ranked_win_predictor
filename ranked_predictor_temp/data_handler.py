import numpy
import pandas as pd
import time
from match_crawler import get_request

API_KEY = '?api_key=RGAPI-86c70ff5-b18e-4101-87b6-f8a10b549c14'
BASE_URL = 'https://euw1.api.riotgames.com/lol/'
BASE_URL_CHAMPIONGG = 'http://api.champion.gg/v2/champions/'
SUMMONER_BY_NAME = 'summoner/v4/summoners/by-name/'
MATCHLIST_BY_ACCOUNT = 'match/v4/matchlists/by-account/'
MATCH_BY_MATCHID = 'match/v4/matches/'
LEAGUE_BY_SUMMONER = 'league/v4/entries/by-summoner/'
MASTERY_BY_SUMMONER = 'champion-mastery/v4/champion-masteries/by-summoner/'

#Generates data, modelled and ready for training/testing neural net
class DataHandler:
    #Instantiate with gameId to get modelled data for single game
    def __init__(self, gameId_input):
        self.gameId = gameId_input
    '''
    get all players from game
    '''
    def get_summonerIds_from_game(self):
        summonerIds = {}
        i=0
        match_data = get_request(BASE_URL+MATCH_BY_MATCHID+self.gameId)
        for data in match_data:
            data = (match_data['participantIdentities'])
            for player in data:
                while i<10:
                    player = data[i]
                    i+=1
                    summoner = (player['player'])
                    summonerIds[player['participantId']]=(summoner['summonerId'])
        return summonerIds
    '''
        get summoner data for ranked games only
        '''
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
    ''' 
    calculate difference in average win rates between the two teams
    to be input into neural net (sigmoid activation)
    '''
    def get_avg_winrate(self, ranked_stats):
        i=0
        team1_wins, team2_wins, team1_losses, team2_losses = 0, 0, 0, 0
        print('calculating average winrate...')
        for summoner_data in ranked_stats:
            wins = summoner_data['wins']
            losses = summoner_data['losses']
            i+=1
            if i<6:
                team1_wins = team1_wins + wins
                team1_losses = team1_losses + losses
                team1_avg_wr = (wins/(wins+losses))*100
            else:
                team2_wins = team2_wins + wins
                team2_losses = team2_losses + losses
                team2_avg_wr = (wins/(wins+losses))*100
        avg_wr = team1_avg_wr - team2_avg_wr
        return avg_wr
    '''
    calculate difference in winstreak, should aid in modelling tilt (playing worse
    because of previous losses, out of form etc). Will also help model for smurfs
    who will likely have large winstreaks or players in form
    '''
    def get_total_winstreak(self, ranked_stats):
        i=0
        team1_winstreak, team2_winstreak = 0,0
        print('calculating winstreaks...')
        for summoner_data in ranked_stats:
            winstreak = summoner_data['hotStreak']
            i+=1
            if i<6 and winstreak == True:
                team1_winstreak += 1
            else:
                team1_winstreak += 0
            if i>5 and winstreak == True:
                team2_winstreak += 1
            else:
                team2_winstreak += 0
        avg_winstreak = team1_winstreak - team2_winstreak
        return avg_winstreak
    #get average champion mastery of all players of a team
    '''
    get participant and champion id from game, find out how much mastery each player has 
    on the champion they picked for current game, calculate totaly mastery among team
    calculate difference in total mastery accross the two teams
    '''
    def get_diff_champion_mastery(self, summonerIds):
        championIds = []
        summonerIds = []
        i, j, team1_combined, team2_combined = 0,0,0,0
        match_data = get_request(BASE_URL+MATCH_BY_MATCHID+self.gameId)
        data = (match_data['participants'])
        for participants in data:
            championIds.append(participants['championId'])
        participantIdentities = (match_data['participantIdentities'])
        for participant in participantIdentities:
            summonerIds.append(participant['player']['summonerId'])
        for summonerId in summonerIds:
            championId = championIds[i] #group summonerId with corresponding championId
            i+=1
            masteryData = get_request(BASE_URL+MASTERY_BY_SUMMONER+summonerId)
            time.sleep(0.5)
            for champion in masteryData:
                if champion.get('championId') == championId:
                    print(champion.get('championPoints'))
                    player_mastery = champion.get('championPoints')
                    if j<5:
                        team1_combined += player_mastery
                    if j>4:
                        team2_combined += player_mastery
                    j+=1
        diff_champion_mastery = team1_combined - team2_combined
        return diff_champion_mastery

    #get average champion winrate for a team
    def get_avg_champion_winrate(self):
        avg_winrate = 53
        return avg_winrate
    '''
    collects data for each player, determining whether they are 'on-role' or 'off-role', where
    generally players that are off-role will play significantly worse relative to players on-role 
    at the same level. Calculates difference in number of off-roles
    '''
    def get_diff_onrole(self):
        diff_onrole = -3
        return diff_onrole

def generate_modelled_data(gameId):
    return None

dh = DataHandler('4019902021')
test = dh.get_ranked5x5_by_summoner(dh.get_summonerIds_from_game())
print(dh.get_avg_winrate(test))
print(dh.get_total_winstreak(test))
print(dh.get_diff_champion_mastery('4019902021'))
