import numpy
import pandas as pd
import time
import consts as cs
import tqdm
from tqdm import tqdm
from match_crawler import get_request
from statistics import mode

#Generates data, modelled and ready for training/testing neural net
class DataHandler:
    #Instantiate with gameId to get modelled data for single game
    def __init__(self, gameId_input):
        self.gameId = gameId_input
        self.match_data = get_request(cs.BASE_URL+cs.MATCH_BY_MATCHID+self.gameId)
    '''
    get all summoner Ids from game
    '''
    def get_summonerIds_from_game(self):
        summonerIds = {}
        i=0
        #match_data = get_request(BASE_URL+MATCH_BY_MATCHID+self.gameId)
        for data in self.match_data:
            data = (self.match_data['participantIdentities'])
            for player in data:
                while i<10:
                    player = data[i]
                    summoner = (player['player'])
                    summonerIds[player['participantId']]=(summoner['summonerId'])
                    i+=1
        return summonerIds
    '''
        get all summoner accountIds from game
        '''
    def get_accountIds_from_game(self):
        accountIds = {}
        i=0
        #match_data = get_request(BASE_URL+MATCH_BY_MATCHID+self.gameId)
        for data in self.match_data:
            data = (self.match_data['participantIdentities'])
            for player in data:
                while i<10:
                    player = data[i]
                    i+=1
                    summoner = (player['player'])
                    accountIds[player['participantId']]=(summoner['accountId'])
        return accountIds
    '''
        get summoner data for ranked games only
        '''
    def get_ranked5x5_by_summoner(self, summonerIds):
        i=1
        ranked_stats = []
        #print('collecting summoner data...')
        for summonerId in summonerIds:
            while i < 11:
                summonerId = summonerIds.get(i)
                i+=1
                summoner_league_data = get_request(cs.BASE_URL+cs.LEAGUE_BY_SUMMONER+summonerId)
                time.sleep(0.2)
                if len(summoner_league_data) == 3:
                    ranked_5x5 = summoner_league_data[2]
                elif len(summoner_league_data) == 2:
                    ranked_5x5 = summoner_league_data[1]
                elif len(summoner_league_data) == 1:
                    ranked_5x5 = summoner_league_data[0]
                else:
                    ranked_5x5 = 'error'
                ranked_stats.append(ranked_5x5)
        return ranked_stats
    ''' 
    calculate difference in average win rates between the two teams
    to be input into neural net (sigmoid activation)
    '''
    def get_avg_winrate(self, ranked_stats):
        i=0
        team1_wins, team2_wins, team1_losses, team2_losses = 0, 0, 0, 0
        #print('calculating average winrate...')
        try:
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
            return round(avg_wr,2)
        except:
            return None
    '''
    calculate difference in winstreak, should aid in modelling tilt (playing worse
    because of previous losses, out of form etc). Will also help model for smurfs
    who will likely have large winstreaks or players in form
    '''
    def get_total_winstreak(self, ranked_stats):
        i=0
        team1_winstreak, team2_winstreak = 0,0
        #print('calculating winstreaks...')
        try:
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
        except:
        #print('total_winstreak error')
            return None
    #get average champion mastery of all players of a team
    '''
        get participant and champion id from game, find out how much mastery each player has 
        on the champion they picked for current game, calculate totaly mastery among team
        calculate difference in total mastery accross the two teams
        '''
    def get_diff_champion_mastery(self, summonerIds):
        #print('calculating difference in champion mastery...')
        championIds,summonerIds = [],[]
        i, j, team1_combined, team2_combined = 0,0,0,0
        #match_data = get_request(BASE_URL+MATCH_BY_MATCHID+self.gameId)
        data = (self.match_data['participants'])
        for participants in data:
            championIds.append(participants['championId'])
        participantIdentities = (self.match_data['participantIdentities'])
        for participant in participantIdentities:
            summonerIds.append(participant['player']['summonerId'])
        for summonerId in summonerIds:
            championId = championIds[i] #group summonerId with corresponding championId
            i+=1 
            masteryData = get_request(cs.BASE_URL+cs.MASTERY_BY_SUMMONER+summonerId)
            time.sleep(0.5)
            for champion in masteryData:
                if champion.get('championId') == championId:
                    player_mastery = champion.get('championPoints')
                    if j<5:
                        team1_combined += player_mastery
                    if j>4:
                        team2_combined += player_mastery
                    j+=1
        diff_champion_mastery = team1_combined - team2_combined
        return diff_champion_mastery

    '''
    Get winning team
    '''
    def get_winning_team(self):
        data = self.match_data['teams']
        for points in data:
            if points.get('win') == 'Win':
                return 1
            elif points.get('win') == 'Fail':
                return 0
        else:
            return None

    '''
    collects data for each player, determining whether they are 'on-role' or 'off-role', where
    generally players that are off-role will play significantly worse relative to players on-role 
    at the same level. Calculates difference in number of off-roles. Has to be calculated on a last 
    20 games basis as no official data regarding roles exists. Note if players don't have ranked games
    in their last 20 matches, this will default to undefined and bias towards the other team.
    This feature will aim to factor in depreciation in skill for players who aren't playing regularly.
    '''
    
    def get_diff_onrole(self, accountIds):
        #print('calculating the difference in number of players on role...')
        i,j, team1_total, team2_total = 1,0,0,0
        participant_by_main_role = {}
        for accountId in accountIds:
            roles_selected = []
            accountId = accountIds.get(i)
            matches_data = get_request(cs.BASE_URL+cs.MATCHLIST_BY_ACCOUNT+str(accountId))
            time.sleep(0.5)
            matches = matches_data.get('matches')
            try:
                for match in matches:
                    if match.get('queue') == 420:
                        roles_selected.append(match.get('lane'))
            except:
                roles_selected.append('UNDEFINED')
            try:
                mode_role = mode(roles_selected)
            except:
                mode_role = 'UNDEFINED'
            participant_by_main_role[i] = mode_role
            participant_role = self.match_data['participants'][j]['timeline']['lane'] #get players role in current game 
            i+=1
            j+=1
            if j<6 and participant_role == mode_role:
                team1_total +=1
            elif j<11 and participant_role == mode_role:
                team2_total +=1
            diff_on_role = team1_total - team2_total         
        return diff_on_role