import os
from googleapiclient.discovery import build

api_key = os.environ.get('yt_api-key')
youtube = build('youtube','v3',developerKey=api_key)

playlist_id = 'PLjpCrb03fbYzleRyi30Y4EkTQHS9rfIME'
videos = []

nextPageToken = None
totalSeconds = 0
while True:
    pl_request = youtube.playlistItems().list(
        part = 'contentDetails',
        playlistId = playlist_id,
        pageToken = nextPageToken, 
        maxResults = 50 # to fetch 50 videos at a time
    )
    pl_response = pl_request.execute()
    # print(pl_response)
    vid_ids = []
    for item in pl_response['items']:
        vid_ids.append(item['contentDetails']['videoId'])

    # write a query to the video resource to grab all of this videos. we can't pass python list of vid_ids so it has to be converted into a strings of comma separted values of all vid_ids
    # print(','.join(vid_ids))
    vid_request = youtube.videos().list(
        part = 'statistics',
        id = ','.join(vid_ids)  # maximum limit is 50 videos i.e., can keep upto 50 video_id
    )
    vid_response =vid_request.execute()

    for item in vid_response['items']:  
        vid_views = int(item['statistics']['viewCount'])
        # print(vid_views)
        vid_id = item['id']
        # print(vid_id)
        yt_link = f'https://www.youtube.com/watch?v={vid_id}'
        # print(yt_link)
        videos.append(
            {
                'views': vid_views,
                'url' : yt_link
            }
        )
        
    nextPageToken = pl_response.get('nextPageToken') # if there r no pages then it will return None

    if not nextPageToken:
        break

videos.sort(key=lambda vid : vid['views'], reverse= True)

for video in videos:
    print(video['url'], video['views'])

