import match_crawler 
import modeller

'''
Script to initiate collecting data, takes a summonder name (string) as a console
input. This allows for collecting data unique to the user. I.e platinum players
will collect data around platinum tier and challengers will get challenger data points
'''

mc = match_crawler.MatchCrawler()

def collect_gameids(summoner, thresh):
    accountId = mc.get_summonerId(summoner)
    matches = mc.get_matches_for_summoner(accountId)
    mc.crawler_writer(matches[0], thresh)
        
def collect_gamedata(sample_size):
    modeller.write_model_data(sample_size)

while(True):
    print('#########################\n DATA COLLECTION SCRIPT \n#########################')
    print('\nfollow prompts to assign values for script to run, type exit to quit \n')
    response = input('do you need to collect game ids? [y/n]: ')
    if response == 'y':
        summoner = input('enter summoner name for entry point: ')
        input_thresh = input('set threshold number of games (recommend 20000): ')
        thresh = int(input_thresh)
        response2 = input('do you need to collect input data? [y/n]: ')
        if response2 == 'y':
            input_sample_size = input('set sample size (runs 1 iteration per 20s): ')
            sample_size = int(sample_size)
            collect_gameids(summoner, thresh)
            collect_gamedata(sample_size)
        elif response2 == 'n':
            collect_gameids(summoner,thresh)
        else:
            print('try again!')
    elif response == 'n':
        response2 = input('do you need to collect input data? [y/n]: ')
        if response2 == 'y':
            input_sample_size = input('set sample size (runs 1 iteration per 20s): ')
            sample_size = int(input_sample_size)
            collect_gamedata(sample_size)
    elif response == 'exit':
        break
    else:
        print('error in script')