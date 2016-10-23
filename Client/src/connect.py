#!/usr/bin/env python2
##
############
##
## Software under MIT licence
##
############

import socket, sys

#######
# Connect

# Server Name
s_name = 'localhost'

# Setver Port
s_port = 36326

# Create a new socket
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
try:
    # Connect to the server
    s.connect( ( s_name, s_port ) )
# Catch error, if any
except socket.error, (value, message):
    print "Sorry, something went grong :/\nTry again later.\n> %s" % (message)
    sys.exit( value )
#
#######

#######
# Communicate
   
# (Future feature: multi service) Send the service of preference
s.sendall( "youtube" )

# If server asks for url give it
if s.recv( 8 ) == 'u':
    s.sendall( raw_input( "URL: " ) )

# Get available formats and give compatibility
# Also, start downloading
data = s.recv( 1024 )

# Here we store formats
formats = []
uformat = 0
if "audio" in data:
    # Parse available formats
    print "Available formats:"
    for format in data.split( "," ):
        
        # Store only audio formats
        if "audio" in format:
            print ">>", format, "<<"
            formats.append( format )
            if uformat < int( format.split()[ 0 ] ):
                uformat = int( format.split()[ 0 ] )
        elif uformat == 0:
            print ">> No available formats <<"
            sys.exit(90)
    # Select best audio format
    #s.sendall( str( uformat ) )
    s.sendall( str( 140 ) )
    # Check if server asks for status and settings
    if s.recv( 8 ) == 's':
        # Send no settings
        s.sendall( '{ok}' )
    
    ####### Delete this >>>>
    test_data_container = ""
    # Start receiving
    while data != "EOS":
        # Get file
        data = s.recv( 4096 )
        test_data_container += data
        # Add to buffer
        # play.enqueue( data )
        print "You got data!!\nThere are %d bytes available!\n" % ( len( test_data_container ) )
else:
    print "Can't get audio from that video :/"
#
#######

#######
# Terminate
print "\nNow exiting..."
s.close()
sys.exit(0)