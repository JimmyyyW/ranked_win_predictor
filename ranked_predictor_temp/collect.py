import match_crawler 
import pandas as pd
from multiprocessing import Process
import sys
import modeller

'''
Script to initiate collecting data, takes a summonder name (string) as a console
input. This allows for collecting data unique to the user. I.e platinum players
will collect data around platinum tier and challengers will get challenger data points
'''

#mc = match_crawler.MatchCrawler()

#summoner = input('enter your summoner name: ')
#accountId = mc.get_summonerId(summoner)
#matches = mc.get_matches_for_summoner(accountId)
#data = pd.DataFrame(mc.crawler_writer(matches[0]))
modeller.write_model_data()

#if __name__=='__main__':
    #p1 = Process(target=modeller.write_model_data(1))
    #p1.start()
    #p2 = Process(target=modeller.write_model_data(6501))
    #p2.start()
    #p3 = Process(target=modeller.write_model_data(13001))
    #p3.start()
    #p4 = Process(target=modeller.write_model_data(19501))
    #p4.start()
    #p5 = Process(target=modeller.write_model_data(26001))
    #p5.start()
    #p6 = Process(target=modeller.write_model_data(32001))
    #p6.start()