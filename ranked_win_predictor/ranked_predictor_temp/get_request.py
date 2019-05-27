from .loggers import req_logger
from . import consts as cs
import requests
import time
'''
backbone of URL requests, 
'''
# initialise outside function so immediate reset to api_key[0] doesn't occur
api_num = 0

def get_request(url):
    global api_num
    trys = 0
    try:
        req = requests.get(url+(cs.API_KEY[api_num]))
        if req.status_code != 200:
            trys += 1
            time.sleep(2)
            req = requests.get(url+(cs.API_KEY[api_num])) #repeat request with new api key
            if trys > 5:
                return None
            elif req.status_code == 404:
                req_logger.error(str(req.status_code) + ' invalid request')
            elif req.status_code == 429:
                req_logger.critical(str(req.status_code)+ ' RATE LIMITED')
                api_num += 1
            elif req.status_code == 403:
                req_logger.critical(str(req.status_code)+ ' check API key')
                api_num += 1
            elif req.status_code == 400:
                req_logger.error(str(req.status_code)+ ' bad request')
                api_num += 1
            else:
                req_logger.info(str(req.status_code)+ ' other none-200')
        if api_num >= len(cs.API_KEY): #check api key within list range every time
            api_num = 0
        if req.status_code == 200:
            req_logger.info(str(req.status_code)+ ' successful request')
        return req.json()
    except:
        req_logger.warn('CHECK API KEY')