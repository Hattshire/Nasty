#!/usr/bin/bash
##
############
##
## Software under MIT licence
##
############

import socket

# Host Name
h_name = socket.gethostname()

# Host Port
h_port = 36326

# Create a new socket
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

# Tell to the socket where to listen
s.bind( ( h_name, h_port ) )

# Start listening
s.listen( 0 )
