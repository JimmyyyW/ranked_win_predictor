import requests
import json
import time
import csv
import progress_bar

API_KEY = '?api_key=RGAPI-c2b39cff-166a-4aca-b536-a1423bc11476'
BASE_URL = 'https://euw1.api.riotgames.com/lol/'
SUMMONER_BY_NAME = 'summoner/v4/summoners/by-name/'
MATCHLIST_BY_ACCOUNT = 'match/v4/matchlists/by-account/'
MATCH_BY_MATCHID = 'match/v4/matches/'

def get_request(url):
    req = requests.get(url+API_KEY)
    if req.status_code != 200:
        print(req.status_code)
       # print(req.headers)
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

    def crawler_writer(self, gameId, thresh=20, pg=0, lb=1):
        participants_in_game = self.get_summoners_from_match(str(gameId))
        print('collecting data..')
        #progress_bar.printProgressBar(0, thresh, prefix='Progress:', suffix='Complete', length=50)
        with open('match_ids2.csv', 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            for participants in participants_in_game:
                while pg<thresh:
                    matches_for_participant = self.get_matches_for_summoner(participants)
                    time.sleep(2.5)
                    for matchId in matches_for_participant:
                        try:
                            players = self.get_summoners_from_match(str(matchId))
                            time.sleep(2.5)
                            for player in players:
                                writer.writerow(self.get_matches_for_summoner(player))
                                print(player)
                                pg+=20
                                print(pg)
                                print(thresh)
                                time.sleep(2.5) #at this tier of recursion 2000 gameIds should have been found
                                #printProgressBar(lb+1, thresh, prefix='Progress:', suffix='Complete', length=50)
                                if pg >= thresh:
                                    print('completed')
                                    csvFile.close()
                                    return None
                                else:
                                    continue
                        except:
                            print('something went wrong')
        print('completed')
        csvFile.close()
        return None

mc = MatchCrawler()
summoner = 'JimmyyW'
accountId = mc.get_summonerId(summoner)
matches = mc.get_matches_for_summoner(accountId)
#print(matches[1])
mc.crawler_writer(matches[0])
