# import os
# from googleapiclient.discovery import build

# api_key = os.environ.get('yt_api-key')
# print(api_key)

# youtube = build('youtube','v3', developerKey = api_key)
# playlist_id = 'UUCezIgC97PvUuR4_gbFUs5g'
# request = youtube.playlistItems().list(part = 'status',playlistId = playlist_id)
# response = request.execute() # lists all the public videos i.e., 'privacyStatus': 'public'
# print(response)

# inorder to view all private/unlisted videos then need to give my script to my yt account data inorder to do this we need to create an oauth client 
# ---------------------- create OAuth Client ID ------------------------------
# install 1. pip install google-auth 2. pip install google-auth-oauthlib

import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# flow = InstalledAppFlow.from_client_secrets_file(
#     "client_secret.json",scopes=["https://www.googleapis.com/auth/youtube.readonly"])

# flow.run_local_server(port=8080, prompt='consent') # as I wasn't getting Refresh Token after multiple times we use prompt='consent'
# once we get authorized with google account we are going to receive several token i.e., there are 2 types of tokens 
# 1. Access Token : have short life span & will get expire shortly after they are issued
# 2. Refresh Token : last much longer & u can use them to fetch new access token for accessing data
# token.pickle stores the user's credentials from previously successful logins

if os.path.exists('token.pickle'):
    print('Loading Credentials From File...')
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)


# Google's Request
from google.auth.transport.requests import Request


# If there are no valid credentials available, then either refresh the token or log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print('Refreshing Access Token...')
        credentials.refresh(Request())
    else:
        print('Fetching New Tokens...')
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secrets.json',
            scopes=[
                'https://www.googleapis.com/auth/youtube.readonly'
            ]
        )

        flow.run_local_server(port=8080, prompt='consent',
                              authorization_prompt_message='')
        credentials = flow.credentials

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)
