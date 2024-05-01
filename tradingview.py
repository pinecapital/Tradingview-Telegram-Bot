import os
import requests
import config
import platform
from dotenv import load_dotenv
from urllib3 import encode_multipart_formdata

# Load environment variables from .env file
load_dotenv()

def login():
    # Check if 'sessionid' is available in environment variables
    if 'sessionid' in os.environ:
        sessionid = os.environ['sessionid']
        print('Using sessionid from environment variables')
    else:
        print('No sessionid found in environment variables')
        return

    headers = {'cookie': 'sessionid=' + sessionid}
    test = requests.request("GET", config.urls["tvcoins"], headers=headers)
    print(test.text)

    if test.status_code == 200:
        print('Session is valid')
        return

    # If session is not valid, proceed to login with username and password
    if 'username' in os.environ and 'password' in os.environ:
        print('session id from environment is invalid, logging in with username and password')
        username = os.environ['username']
        password = os.environ['password']

        payload = {
            'username': username,
            'password': password,
            'remember': 'on'
        }
        body, contentType = encode_multipart_formdata(payload)
        userAgent = 'TWAPI/3.0 (' + platform.system() + '; ' + platform.version() + '; ' + platform.release() + ')'
        print(userAgent)
        login_headers = {
            'origin': 'https://www.tradingview.com',
            'User-Agent': userAgent,
            'Content-Type': contentType,
            'referer': 'https://www.tradingview.com'
        }
        login_response = requests.post(config.urls["signin"], data=body, headers=login_headers)
        cookies = login_response.cookies.get_dict()

        if "sessionid" in cookies:
            sessionid = cookies["sessionid"]
            os.environ['sessionid'] = sessionid  # Optionally store the new sessionid back to environment
            print('New sessionid obtained and stored in environment')
        else:
            print('Failed to log in and obtain a new sessionid')
