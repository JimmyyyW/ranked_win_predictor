import time
import pandas as pd
import consts as cs
import data_handler as dhdlr
from get_request import get_request
from loggers import mod_logger
from modeller import generate_modelled_data


def get_live_game(summoner):
    #get summonerId from player name
    req = get_request(cs.BASE_URL+cs.SUMMONER_BY_NAME+summoner)
    summonerId = req['id']

    #get live game for player
    game = get_request(cs.BASE_URL+cs.LIVE_GAME_BY_SUMMONER+(str(summonerId)))
    gameId = game['gameId']

    #get summonerIds and champ from live game put in dict
    i, summonerIds = 1, {}
    j, champIds = 1, {}
    participants = game['participants']
    for participant in participants:
        summonerIds[i]=participant['summonerId']
        i+=1
        champIds[j]=participant['championId']
        j+=1

    #initialise datahandler to re-use functions
    dh = dhdlr.DataHandler(gameId)
    #ranked 5x5
    rank5x5 = dh.get_ranked5x5_by_summoner(summonerIds)

    #get average winrate
    avg_wr = dh.get_avg_winrate(rank5x5)
    time.sleep(0.25)

    #get average winstreak
    avg_ws = dh.get_total_winstreak(rank5x5)
    time.sleep(0.25)

    #get diff champ mastery
    i, j, team1_combined, team2_combined = 1,1,0,0
    for summoner in summonerIds:
        summonerId = summonerIds.get(i)
        champ = champIds.get(i)
        mastery = get_request(cs.BASE_URL+cs.MASTERY_BY_SUMMONER+summonerId)
        for champion in mastery:
            if champion.get('championId') == champ:
                player_mastery = champion.get('championPoints')
                if j<5:
                    team1_combined += player_mastery
                if j>4:
                    team2_combined += player_mastery
                j+=1
    avg_mstry = team1_combined - team2_combined
            
    #get diff onrole by getting account ids then re-using function. No current means of getting
    #from live games, will assume 0 for testing
    avg_onrle = 0

    
    #format data for neural net
    data = {
            "avg_wr":[avg_wr],
            "avg_ws":[avg_ws],
            "avg_mstry":[avg_mstry],
            "avg_onrle":[avg_onrle],
        }
    df = pd.DataFrame(data)
    return df
