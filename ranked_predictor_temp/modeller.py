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
        time.sleep(0.25)
        accountIds = dh.get_accountIds_from_game()
        time.sleep(0.25)
        summonerIds = dh.get_summonerIds_from_game()
        time.sleep(0.25)
        ranked_5x5 = dh.get_ranked5x5_by_summoner(summonerIds)
        time.sleep(0.25)
        avg_wr = dh.get_avg_winrate(ranked_5x5)
        time.sleep(0.25)
        avg_ws = dh.get_total_winstreak(ranked_5x5)
        time.sleep(0.25)
        avg_mstry = dh.get_diff_champion_mastery(gameId)
        time.sleep(0.25)
        avg_onrle = dh.get_diff_onrole(accountIds)
        result = dh.get_winning_team()
        data = {
            "avg_wr":[avg_wr],
            "avg_ws":[avg_ws],
            "avg_mstry":[avg_mstry],
            "avg_onrle":[avg_onrle],
            "result":[result]
        }
        df = pd.DataFrame(data)
        for stats in data:
            if stats.values() == None or stats.values() == 'NaN':
                mod_logger.info('null model data')
            else:
                mod_logger.info('success')
    except:
        mod_logger.info('modeller failure')
    return df

def write_model_data(sample_size=50):
    model_data = pd.DataFrame()
    df = pd.read_csv("game_ids.csv")
    with tqdm(total=sample_size) as pbar:
        for index, row in df.iterrows():
            model_data = model_data.append(generate_modelled_data(str(row['GameId'])))
            time.sleep(0.1)
            pbar.update(1)
            if index >= sample_size:
                break
    model_data.to_csv('modelled_data.csv')
    print(model_data.head())
    return None

#write_model_data()