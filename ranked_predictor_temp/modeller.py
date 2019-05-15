
import os
from os import path
import logging
from logging import config
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
req_logger = logging.getLogger('modeller')

import pandas
import tqdm
from tqdm import tqdm
import data_handler as dhdlr

'''
using data handler functions, iterate through gameIds 
'''
def generate_modelled_data(gameId):
    dh = dhdlr.DataHandler(gameId)
    accountIds = dh.get_accountIds_from_game()
    summonerIds = dh.get_summonerIds_from_game()
    ranked_5x5 = dh.get_ranked5x5_by_summoner(summonerIds)
    print(dh.get_avg_winrate(ranked_5x5))
    print(dh.get_total_winstreak(ranked_5x5))
    print(dh.get_diff_champion_mastery(gameId))
    print(dh.get_diff_onrole(accountIds))