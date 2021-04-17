import requests
import json

def get_access_from_refresh(refresh_file="refresh_token.txt", conskey_file="consumer_key.txt"):

    refresh = ""
    with open(refresh_file, 'r') as fhand:
        refresh = fhand.read().replace('\n', '')

    
    conskey = ""
    with open(conskey_file, "r") as fhand:
        conskey = fhand.read().replace("\n", "")

    callback = "http://localhost"

    url = "https://api.tdameritrade.com/v1/oauth2/token"
    data = {'grant_type': 'refresh_token', 'refresh_token': refresh, 'client_id': conskey, 'redirect_uri': callback}
    req = requests.post(url, data=data)
    jsondata = json.loads(req.text)

    print(jsondata)

    return jsondata['access_token']

# For testing
if __name__ == "__main__":
    print(get_access_from_refresh())