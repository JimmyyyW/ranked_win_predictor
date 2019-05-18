import pandas
import tqdm
from tqdm import tqdm
from loggers import mod_logger
import data_handler as dhdlr


'''
using data handler functions, iterate through gameIds 
'''
def generate_modelled_data(gameId):
    try: 
        dh = dhdlr.DataHandler(gameId)
        accountIds = dh.get_accountIds_from_game()
        summonerIds = dh.get_summonerIds_from_game()
        ranked_5x5 = dh.get_ranked5x5_by_summoner(summonerIds)
        print(dh.get_avg_winrate(ranked_5x5))
        print(dh.get_total_winstreak(ranked_5x5))
        print(dh.get_diff_champion_mastery(gameId))
        print(dh.get_diff_onrole(accountIds))
    except:
        mod_logger.WARN('modeller failure')