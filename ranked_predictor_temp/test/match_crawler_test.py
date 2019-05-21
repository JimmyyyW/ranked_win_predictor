import unittest
from unittest import mock
import json
import match_crawler
from match_crawler import MatchCrawler

class TestDataHandler(unittest.TestCase):

    def get_request_reqstatuscode_is_404_if_bad_url(self):
        req = match_crawler.get_request('https://www.definitelynotarealurl.com/return/404')
        print(req)
        return None

