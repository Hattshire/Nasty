#!/usr/bin/bash
##
############
##
## Software under MIT licence
##
############

import socket

# Server Name
s_name = 'localhost'

# Setver Port
s_port = 36326

# Create a new socket
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

# Connect to the server
s.connect( ( s_name, s_port ) )
print "Conncted!1!!"
