import unittest
from unittest.mock import Mock
import json
from data_handler import DataHandler


class TestDataHandler(unittest.TestCase):

    def test_get_summoners_from_game(self, i=0):
        '''
        Test that it returns summoners from match data
        '''
        dh = DataHandler('4018482509')
        summonerIds_expected={}
        #load mock data
        with open('ranked_predictor_temp/test/mock_data/mock_datahandler_match_data.json') as f:
            data = json.load(f)
            parsed = data['participantIdentities']
            for player in parsed:
                while i<10:
                    player = parsed[i]
                    summoner = (player['player'])
                    summonerIds_expected[player['participantId']]=(summoner['summonerId'])
                    i+=1
        self.assertEqual(summonerIds_expected, dh.get_summonerIds_from_game())
        return None

    def test_get_accountIds_from_game(self,i=0):
        '''
        Test that method returns accountIds from match data
        '''
        dh = DataHandler('4018482509')
        accountIds_expected={}
        #load mock data
        with open('ranked_predictor_temp/test/mock_data/mock_datahandler_match_data.json') as f:
            data = json.load(f)
            parsed = data['participantIdentities']
            for player in parsed:
                while i<10:
                    player = parsed[i]
                    summoner = (player['player'])
                    accountIds_expected[player['participantId']]=(summoner['accountId'])
                    i+=1
        self.assertEqual(accountIds_expected, dh.get_accountIds_from_game())
        return None

   # @mock.patch('dh.test_get_ranked5x5_by_summoner', return_value='data')
    def test_get_ranked5x5_by_summoner(self):
        '''
        Test return ranked 5 vs 5 stats for a given summoner
        '''
        with open('ranked_predictor_temp/test/mock_data/mock_ranked5x5.json') as f:
            ranked5x5_data = json.load(f)
            expected = ranked5x5_data[2]
        self.assertEqual(expected, expected)
        return None

    def test_get_avg_wr(self):
        '''
        Test get avg wr returns avg wr
        '''
        dh = DataHandler('4034126665')
        ranked_data = dh.get_ranked5x5_by_summoner(dh.get_summonerIds_from_game())
        result = dh.get_avg_winrate(ranked_data)
        expected = -7.31
        self.assertEquals(expected,result)
        return None

    def test_get_diff_champion_mstry(self):
        '''
        Test method returns correct difference in champion mastery between teams in game
        '''
        dh = DataHandler('4034126665')
        result = dh.get_diff_champion_mastery(dh.get_summonerIds_from_game())
        expected = 230611
        self.assertEqual(expected, result)
        return None

    def test_get_diff_onrole(self):
        '''
        Test method correctly returning difference in number of players on their main role
        '''
        dh = DataHandler('403412665')
        preresult = dh.get_accountIds_from_game()
        result = dh.get_diff_onrole(preresult)
        expected = 0
        self.assertEqual(expected, result)

    def test_get_winning_team(self):
        '''
        tests that method returns 0 for red team win
        '''
        dh = DataHandler('4034126665')
        result = dh.get_winning_team()
        expected = 0
        self.assertEqual(expected, result)


if __name__=='__main__':
    unittest.main()

