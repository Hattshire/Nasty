#!/usr/bin/bash
##
############
##
## Software under MIT licence
##
############

import youtube_dl

url = 'https://www.youtube.com/watch?v=We11XkhZu7U'

# Get info from video url
def get_info(url):
    # 'video' will store YDL's object
    video = youtube_dl.YoutubeDL()

    # We get the video's info
    with video as obj:
        video = obj.extract_info( url, download = False )

    # Return info
    return video
