import unittest
from unittest import mock
import json
import match_crawler

class TestMatchCrawler(unittest.TestCase):
    @mock.patch('match_crawler.get_request')
    def get_request_reqstatuscode_is_404_if_bad_url(self, mock_url):
        request = match_crawler.get_request(mock_url)
        print(request)
        return None

if __name__=='__main__':
    unittest.main()