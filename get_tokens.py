import requests
import urllib
import requests
from splinter import Browser
import json
import os

"""

The overall flow of working with TD ameritrade access tokens:

1. Get Auth Token by Logging in with Browser via get_auth_token_from_login()
2. Get access token and refresh token
3. Use access token for all other API queries
4. If access token expires, use refresh token to get access code token and go to 3
5. If refresh token expires, go to 1

"""

conskey_file = "consumer_key.txt"
conskey = ""
with open(conskey_file, "r") as fhand:
    conskey = fhand.read().replace("\n", "")

callback = "http://localhost"

path_to = os.path.abspath("chromedriver")

executable_path = {'executable_path':path_to}

browser = Browser('chrome', **executable_path, headless = False)


# Get authentication code
# Takes you to a page where you can fill in credentials to get an auth code.
# After getting the code from the "code=" portion of the URL, use urllib.parse.unquote(codestring) to get the parsed version
def get_auth_code_from_login():

    method = 'GET'
    url = "https://auth.tdameritrade.com/auth?"

    payload = {'response_type':'code', 'redirect_uri':callback, 'client_id':conskey + '@AMER.OAUTHAP'}

    built_url = requests.Request(method, url, params = payload).prepare()
    built_url = built_url.url

    # Go to URL

    browser.visit(built_url)

# Get access token and refresh token (access token for all api requests, refresh tokens for getting a new access token)
def get_tokens_from_auth_code(auth_code):

    url = "https://api.tdameritrade.com/v1/oauth2/token"
    data = {'grant_type': 'authorization_code', 'access_type': 'offline', 'code': auth_code, 'client_id': conskey, 'redirect_uri': callback}
    req = requests.post(url, data=data)
    jsondata = json.loads(req.text)

    return jsondata['access_token'], jsondata['refresh_token']

if __name__ == "__main__":

    get_auth_code_from_login()
    auth_code = input("Input auth code from url: ")
    auth_code = urllib.parse.unquote(auth_code)

    access_token, refresh_token = get_tokens_from_auth_code(auth_code)

    with open("access_token.txt", "w") as fhand:
        fhand.write(access_token)
    with open("refresh_token.txt", "w") as fhand:
        fhand.write(refresh_token)

    print("Wrote out tokens to files.")
