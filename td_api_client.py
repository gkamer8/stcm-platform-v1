import requests
import json

import get_access_from_refresh

ACC_NUM = 454651642

class TDAPIClient():

    def __init__(self, access_token_file='access_token.txt', refresh_token_file='refresh_token.txt'):

        self.access_token = ''
        with open(access_token_file, 'r') as fhand:
            self.access_token = fhand.read().replace('\n', '')

        self.refresh_token = ''
        with open(refresh_token_file, 'r') as fhand:
            self.refresh_token = fhand.read().replace('\n', '')

        self.refresh_token_file = refresh_token_file
        self.access_token_file = access_token_file

        self.authorization_header = {'Authorization': 'Bearer ' + str(self.access_token)}

    def update_access_token(self):
        access_token = get_access_from_refresh.get_access_from_refresh(refresh_file=self.refresh_token_file)
        with open(self.access_token_file, 'w') as fhand:
            fhand.write(access_token)

        self.access_token = access_token
        self.authorization_header = {'Authorization': 'Bearer ' + str(self.access_token)}

    # https://developer.tdameritrade.com/account-access/apis/get/accounts/%7BaccountId%7D-0
    def get_account(self, attempt=0):
        url = "https://api.tdameritrade.com/v1/accounts/" + str(ACC_NUM)
        payload = {}
        r = requests.get(url, params=payload, headers=self.authorization_header)
        data = json.loads(r.text)
        
        if 'error' in data:
            if attempt >= 1:
                print("Error on second attempt. Returning error.")
                return {'error': 'TD error'}
            print("Error! Getting new access token and retrying.")
            self.update_access_token()
            return self.get_account(attempt=1)

        data = data['securitiesAccount']
        to_return = {
            'liquidationValue': data['currentBalances']['liquidationValue'],
            'longMarketValue': data['currentBalances']['longMarketValue'],
            'cashBalance': data['currentBalances']['cashBalance'],
            'moneyMarketFund': data['currentBalances']['moneyMarketFund']
        }

        return to_return

    def get_positions(self, attempt=0):
        url = "https://api.tdameritrade.com/v1/accounts/" + str(ACC_NUM)
        payload = {'fields': 'positions'}
        r = requests.get(url, params=payload, headers=self.authorization_header)
        data = json.loads(r.text)

        if 'error' in data:
            if attempt >= 1:
                print("Error on second attempt. Returning error.")
                return {'error': 'TD error'}
            print("Error! Getting new access token and retrying.")
            self.update_access_token()
            return self.get_positions(attempt=1)

        data = data['securitiesAccount']
        to_return = {'positions': []}
        for position in data['positions']:
            filtered = {
                'symbol': position['instrument']['symbol'],
                'assetType': position['instrument']['assetType'],  # Almost always "EQUITY"
                'averagePrice': position['averagePrice'],
                'marketValue': position['marketValue'],
                'longQuantity': position['settledLongQuantity'],
                'shortQuantity': position['settledShortQuantity']
            }
            to_return['positions'].append(filtered)
        return to_return


if __name__ == "__main__":

    client = TDAPIClient()
    print(client.get_account())
    # print(client.get_positions())