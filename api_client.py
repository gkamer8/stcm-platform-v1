import json
import requests


"""

Current API is from polygon.io
Account is the stcm email with TD Ameritrade password

Api key is stored in api_key.txt by default. (You have to make this yourself)

This client is made to be the only part of the code that depends on Polygon.io.
If we ever wanted to switch in the future, the functions that are here should be preserved,
but their implementations will change (except maybe for certain functions like query()
and makeUrl())


"""

DEBUG = True  # Prints out things in certain functions and runs from main

BASE_URL = 'https://api.polygon.io'

# Returns object from json load of request of url
def query(url):
    if DEBUG:
        print('Querying: ' + url)
    req = requests.get(url)
    return json.loads(req.text)


class APIClient():

    def __init__(self, api_key_file='api_key.txt'):
        
        # Get API key

        self.api_key = ''
        with open(api_key_file, 'r') as fhand:
            self.api_key = fhand.read().replace('\n', '')
    
    # Makes request url from the path and a dictionary of arguments
    def makeUrl(self, path, args):
        path = BASE_URL + path + "?apiKey=" + self.api_key
        for arg in args:
            path += "&" + str(arg) + "=" + str(args[arg])
        return path
    
    # Saves the results of a function call into a file
    # By default, the file is the same name as the function
    def write(self, func, *args, **kwargs):
        res = func(*args, **kwargs)
        with open('data/' + func.__name__ + ".json", 'w') as fhand:
            json.dump(res, fhand)
    
    # Same as write except takes a result instead of a function
    # Data folder path is already included along with .json
    def write_res(self, res, outfile):
        with open('data/' + outfile + ".json", 'w') as fhand:
            json.dump(res, fhand)
    
    # Returns list of all stock tickers
    def get_all_stock_tickers(self, max_tick=1e10):
        page = 1
        path = "/v2/reference/tickers"
        perpage = 1000
        args = {
            'page': page,
            'perpage': perpage,
            'market': 'stocks'
        }
        ticker_list = []
        while True:
            res = query(self.makeUrl(path, args))
            count = res['count']
            
            ticker_list.extend([x['ticker'] for x in res['tickers']])
            
            if count <= perpage * page or max_tick <= perpage * page:
                break
            page += 1
            args['page'] = page
        
        return ticker_list

    # Returns true if the ticker is an actual stock ticker
    # use_cache determines whether to call get_all_stock_tickers or go to /data
    def is_a_stock_ticker(self, ticker, use_cache=True):
        
        if use_cache:
            all_tickers = json.load(open('data/get_all_stock_tickers.json','r'))
        else:
            all_tickers = self.get_all_stock_tickers()
        
        return ticker.upper() in all_tickers
    
    # Searches the API for a ticker
    # Returns list of dictionaries with ticker, name, and exchange
    def seach_for_ticker(self, search, max_tick=1e10, start_page=1):
        page = start_page
        path = "/v2/reference/tickers"
        perpage = 1000
        args = {
            'page': page,
            'perpage': perpage,
            'sort': 'ticker',
            'search': search,
        }
        result_list = []
        while True:
            res = query(self.makeUrl(path, args))
            count = res['count']
            
            result_list.extend([
                                {
                                    'ticker': x['ticker'],
                                    'name': x['name'],
                                    'exchange': x['primaryExch']
                                } for x in res['tickers']])
            
            if count <= perpage * page or max_tick <= perpage * page:
                break
            page += 1
            args['page'] = page
        
        return result_list

if __name__ == '__main__':
    if DEBUG:
        # For testing
        my_client = APIClient()
        # ticks = my_client.get_all_stock_tickers(max_tick=2000)

        my_client.write(my_client.get_all_stock_tickers, max_tick=2000)

    
