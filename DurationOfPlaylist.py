import os
from googleapiclient.discovery import build
import re
from datetime import timedelta

import re._compiler

# -------------------------------------- PART 2: Fetch frist 5 playlist from a channel ---------------------------------------------
# youtube = build('youtube','v3',developerKey=api_key)
# pl_request = youtube.playlists().list(
#     part = 'contentDetails, snippet',
#     channelId = 'UCCezIgC97PvUuR4_gbFUs5g'
# )
# pl_response = pl_request.execute() # returns only 5 playlists from the channel
# # print(pl_response)
# count=0
# for item in pl_response['items']:
#     print(item)
#     count+=1
#     print(count)

# -------------------------------------- PART 3: loop through all the vedios within the playlist ---------------------------------------------
# for 'title': 'Pandas Tutorials' and 'id': ''
api_key = os.environ.get('yt_api-key')
youtube = build('youtube','v3',developerKey=api_key)

hours_pattern = re.compile(r'(\d+)H')
Minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')
# Page Token : which will allow us to get all the results one page at a time. Each page give the reference to the next page & we can keep track of which page we are on using that page token

nextPageToken = None
totalSeconds = 0
while True:
    pl_request = youtube.playlistItems().list(
        part = 'contentDetails',
        playlistId = 'PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS',
        pageToken = nextPageToken, 
        maxResults = 50 # to fetch 50 videos at a time
    )
    pl_response = pl_request.execute()
    # print(pl_response)
    vid_ids = []
    for item in pl_response['items']:
        # print(item)
        # video_id = item['contentDetails']['videoId']
        # print(video_id)
        vid_ids.append(item['contentDetails']['videoId'])

    # write a query to the video resource to grab all of this videos. we can't pass python list of vid_ids so it has to be converted into a strings of comma separted values of all vid_ids
    print(','.join(vid_ids))
    vid_request = youtube.videos().list(
        part = 'contentDetails',
        id = ','.join(vid_ids)  # maximum limit is 50 videos i.e., can keep upto 50 video_id
    )
    vid_response =vid_request.execute()

    for item in vid_response['items']:  
        # print(item)
        duration = item['contentDetails']['duration']
        # print(duration)
        hours = hours_pattern.search(duration)
        minutes = Minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)

        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0
        # print(hours,minutes,seconds)

        video_seconds = timedelta(
            hours= hours,
            minutes= minutes,
            seconds= seconds
        ).total_seconds()

        # print(video_seconds) # this is just for 5 videos
        totalSeconds += video_seconds
        
        print()
        
    nextPageToken = pl_response.get('nextPageToken') # if there r no pages then it will return None

    if not nextPageToken:
        break

print(totalSeconds)

# divmod : allows us to divide 2 numbers & it returns a tuple of the quotient and the remainder
totalSeconds=int(totalSeconds) # converting it to int as totalseconds is a float
minutes, seconds = divmod(totalSeconds, 60)
hours, minutes = divmod(minutes, 60)
print(f'{hours}:{minutes}:{seconds}')
