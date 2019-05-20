import logging
import logging.config
import os
from os import path
from loggers import req_logger
import requests
import json
import time
import csv
import tqdm
import pandas as pd
import consts as cs
from tqdm import tqdm

api_num = 0
'''
backbone of URL requests, 
'''
# initialise outside function so immediate reset to api_key[0] doesn't occur
def get_request(url):
    global api_num
    req = requests.get(url+(cs.API_KEY[api_num]))
    if req.status_code != 200:
        time.sleep(2)
        req = requests.get(url+(cs.API_KEY[api_num])) #repeat request with new api key
        if req.status_code == 404:
            req_logger.error(str(req.status_code) + ' invalid request')
        elif req.status_code == 429:
            req_logger.critical(str(req.status_code)+ ' RATE LIMITED')
            api_num += 1
        elif req.status_code == 403:
            req_logger.critical(str(req.status_code)+ ' check API key')
            api_num += 1
        elif req.status_code == 400:
            req_logger.error(str(req.status_code)+ ' bad request')
            api_num += 1
        else:
            req_logger.info(str(req.status_code)+ ' other none-200')
    if api_num >= len(cs.API_KEY): #check api key within list range every time
        api_num = 0
    if req.status_code == 200:
        req_logger.info(str(req.status_code)+ ' successful request')
    return req.json()

class MatchCrawler:
    def get_summonerId(self,summoner):
        req = get_request(cs.BASE_URL+cs.SUMMONER_BY_NAME+summoner)
        summonerId = req['accountId']
        return summonerId
    
    def get_matches_for_summoner(self,accountId):
        matchlist = get_request(cs.BASE_URL+cs.MATCHLIST_BY_ACCOUNT+accountId)
        matches = matchlist['matches']
        games_for_summoner = []
        for match in matches:
            games_for_summoner.append(match['gameId'])
        return games_for_summoner

    def get_summoners_from_match(self,gameId):
        matchInfo = get_request(cs.BASE_URL+cs.MATCH_BY_MATCHID+gameId)
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

    def crawler_writer(self, gameId, thresh=40000, n=0, lb=1):
        df = pd.DataFrame()
        participants_in_game = self.get_summoners_from_match(str(gameId))
        print('collecting data..')
        with tqdm(total=thresh) as pbar:
            for participants in participants_in_game:
                while n<thresh:
                    matches_for_participant = self.get_matches_for_summoner(participants)
                    time.sleep(1.5)
                    for matchId in matches_for_participant:
                        try:
                            players = self.get_summoners_from_match(str(matchId))
                            time.sleep(1.5)
                            for player in players:
                                gameId = self.get_matches_for_summoner(player)
                                n+=100
                                df_temp = pd.DataFrame(gameId,columns=['GameId'])
                                df = df.append(df_temp, ignore_index=True)
                                time.sleep(1.5) #at this tier of recursion 2000 gameIds should have been found
                                df.drop_duplicates()
                                pbar.update(100) 
                                if n >= thresh:
                                    print('completed')
                                    df.to_csv('game_ids.csv')
                                    return df
                                else:
                                    continue
                        except:
                            continue
        return None
