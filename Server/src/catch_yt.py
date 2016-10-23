#!/usr/bin/env python2
##
############
##
## Software under MIT licence
##
############

import youtube_dl
import requests
import processing

# Main processing object
class Yt:
    def __init__( self, buffer_len = 1024 ):
        # YoutubeDL object
        self.ydl = youtube_dl.YoutubeDL( params = { 'extract_flat': 'in_playlist' } )
        
        # Temporal/Test variables
        self.video = None
        self.url = None
        self.formats = None
        self.video_count = 0
        
        self.downloader = None
        self.buffer_len = buffer_len * 128
        
    # Get info from video url
    def get_info( self, url ):
        # We get the video's info
        self.video = self.ydl.extract_info( url, download = False )
        if 'entries' in self.video:
            print "Playlist detected"
            self.video_count = len( self.video[ 'entries' ] )
        else:
            print "Video detected"
            self.video_count = 1
    
    # Download a chunk of the audio or video and return it
    def get_audio( self, position = 0, step = 0, format = 0 ):
        format = self.id_to_format( format )
        bitrate = format['abr']
        
        if self.downloader == None:
            self.downloader = Downloader( format[ 'url' ] )
        audio = self.downloader.chunk_download( start = step * self.buffer_len,
                                                len = self.buffer_len )
        return audio if len( audio ) > 0 else "EOS"
        
    # Get available formats and put them on a string
    def get_format_string( self ):
        formats_s = ""
        if self.video != None:
            for stream in self.video[ 'formats' ]:
                formats_s += stream[ 'format' ] + \
                    ( "" if self.video[ 'formats' ][ -1 ] == stream else "," )
            return formats_s
        else:
            return "Error: Non Initialized"
            
    # Return the format's components from a format id
    def id_to_format( self, id ):
        for format in self.video[ 'formats' ]:
            if format[ 'format' ].split()[ 0 ] == str( id ):
                return format
        return None
    def get_title( self ):
        return self.video[ 'title' ]
    
################
# A Video object
class Video:
    def __init__( self ):
        self.unknown = None
        
###################
# A Playlist object
class Playlist( Video ):
    def __init__( self ):
        self.unknown = None
        
class Downloader:
    def __init__( self, url ):
        self.url = url
        
    def chunk_download( self, start = 0, end = None, len = None ):
        head = { 'Range': 'bytes=' + \
                str( start ) + \
                '-' + \
                ( str( end ) if end != None else ( str( start + len-1 ) if len != None else '' ) )
               }
        chunk = requests.get( self.url, headers = head )
        return chunk.content
        