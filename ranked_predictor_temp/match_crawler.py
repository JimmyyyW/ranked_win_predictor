import requests
import json
import time
import csv

API_KEY = '?api_key=RGAPI-86c70ff5-b18e-4101-87b6-f8a10b549c14'
BASE_URL = 'https://euw1.api.riotgames.com/lol/'
SUMMONER_BY_NAME = 'summoner/v4/summoners/by-name/'
MATCHLIST_BY_ACCOUNT = 'match/v4/matchlists/by-account/'
MATCH_BY_MATCHID = 'match/v4/matches/'

def get_request(url):
    req = requests.get(url+API_KEY)
    if req.status_code != 200:
        print(req.status_code)
    return req.json()

class MatchCrawler:
    def get_summonerId(self,summoner):
        req = get_request(BASE_URL+SUMMONER_BY_NAME+summoner)
        summonerId = req['accountId']
        return summonerId
    

    def get_matches_for_summoner(self,accountId):
        matchlist = get_request(BASE_URL+MATCHLIST_BY_ACCOUNT+accountId)
        matches = matchlist['matches']
        games_for_summoner = []
        for match in matches:
            games_for_summoner.append(match['gameId'])
        return games_for_summoner

    def get_summoners_from_match(self,gameId):
        matchInfo = get_request(BASE_URL+MATCH_BY_MATCHID+gameId)
        participants = matchInfo['participantIdentities']
        summoners = []
        for player in participants:
            summoners.append(player['player']['accountId'])
        return summoners
    '''
    using one account id to get matches
    for each of those matches get more accountids
    for each iteration save all matches to csv until threshold reached
    '''

    def crawler_writer(self, gameId):
        participants_in_game = self.get_summoners_from_match(str(gameId))
        branch = []
        i=0
        j=0
        for participants in participants_in_game:
            while i<2:
                print('collecting data....')
                matches_for_participant = self.get_matches_for_summoner(participants)
                for matchId in matches_for_participant:
                    while j<2:
                        branch = self.get_summoners_from_match(str(matchId))
                        time.sleep(2)
                        i=i+1
                        j=j+1
                        for leafs in branch:
                            try:
                                matches_for_participant.append(self.get_matches_for_summoner(leafs))
                                time.sleep(2)
                            except:
                                print('something went wrong')
                            with open('match_ids.csv', 'w') as csvFile:
                                writer = csv.writer(csvFile)
                                writer.writerow(matches_for_participant)
                            csvFile.close()
                time.sleep(2)
                print('completed')
        return None

#mc = MatchCrawler()
summoner = 'JimmyyW'
#accountId = mc.get_summonerId(summoner)
#matches = mc.get_matches_for_summoner(accountId)
#print(matches[1])
#mc.crawler_writer(matches[1])
