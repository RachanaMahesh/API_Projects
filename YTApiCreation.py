# To keep it safe keep it under environment variable
import os
from googleapiclient.discovery import build
import re
from datetime import timedelta

import re._compiler

api_key = os.environ.get('yt_api-key')
print(api_key)
#-------------------------------------- PART 1 --------------------------------------------
youtube = build('youtube','v3',developerKey=api_key)
request = youtube.channels().list(
    part = 'statistics',
    forUsername = 'schafer5'
)
response = request.execute()
print(response)

