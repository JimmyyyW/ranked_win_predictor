import pandas as pd
import tqdm
from tqdm import tqdm
from loggers import mod_logger
import data_handler as dhdlr
import time

#using data handler functions, iterate through gameIds 
def generate_modelled_data(gameId):
    df = pd.DataFrame(columns=['avg_wr','avg_ws','avg_mstry','avg_onrle'])
    try: 
        dh = dhdlr.DataHandler(gameId)
        accountIds = dh.get_accountIds_from_game()
        summonerIds = dh.get_summonerIds_from_game()
        ranked_5x5 = dh.get_ranked5x5_by_summoner(summonerIds)
        avg_wr = dh.get_avg_winrate(ranked_5x5)
        avg_ws = dh.get_total_winstreak(ranked_5x5)
        avg_mstry = dh.get_diff_champion_mastery(gameId)
        avg_onrle = dh.get_diff_onrole(accountIds)
        data = {
            "avg_wr":[avg_wr],
            "avg_ws":[avg_ws],
            "avg_mstry":[avg_mstry],
            "avg_onrle":[avg_onrle]
        }
        df = pd.DataFrame(data)
        for stats in data:
            if stats.values() == None:
                mod_logger.info('null model data')
            else:
                mod_logger.info('success')
    except:
        mod_logger.info('modeller failure')
    return df

def write_model_data():
    model_data = pd.DataFrame()
    df = pd.read_csv("match_ids.csv")
    with tqdm(total=20) as pbar:
        for index, row in df.iterrows():
            model_data = model_data.append(generate_modelled_data(str(row['GameId'])))
            time.sleep(2)
            pbar.update(1)
            if index >= 20:
                break
    model_data.to_csv('modelled_data.csv')
    print(model_data.head())
    return None

#generate_modelled_data('4031513331')            
write_model_data()