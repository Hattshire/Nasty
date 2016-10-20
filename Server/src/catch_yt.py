#!/usr/bin/env python2
##
############
##
## Software under MIT licence
##
############

import youtube_dl

# Main processing object
class Yt:
    def __init__(self):
        # YoutubeDL object
        self.ydl = youtube_dl.YoutubeDL()
        
        # Temporal/Test variables
        self.video = None
        self.url = None
        self.formats = None
        
    # Get info from video url
    def get_info( self, url ):
        # We get the video's info
        self.video = self.ydl.extract_info( url, download = False )
    
    # Download a chunk of the audio or video and return it
    def get_audio( self, position = 0, buffer = 4096, step = 0, format = 0 ):
        print format
        format = self.id_to_format( format )
        bitrate = format['abr']
        try:
            audio = format['url'][((position*bitrate)+step*buffer)-((position*bitrate)+(step*buffer)+buffer)]
        except:
            audio = ""
        return audio if len( str( audio ) ) > 0 else "EOS"
    # Get available formats and put them on a string
    def get_format_string( self ):
        formats_s = ""
        if self.video != None:
            for stream in self.video['formats']:
                formats_s += stream['format'] + ( "" if self.video['formats'][-1] == stream else "," )
            return formats_s
        else:
            return "Error: Non Initialized"
    # Return the format's components from a format id
    def id_to_format( self, id ):
        for format in self.video['formats']:
            
            if format['format'].split()[0] == str( id ):
                return format
        return None
    def get_title(self):
        return self.video['title']
    
################
# A Video object
class video:
    def __init__(self):
        self.unknown = None
        
###################
# A Playlist object
class playlist:
    def __init__(self):
        self.unknown = None