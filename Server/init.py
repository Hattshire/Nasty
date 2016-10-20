#!/usr/bin/env python2
##
############
##
## Software under MIT licence
##
############

# Putting "src" to PATH
import os, sys, inspect, Queue, threading
cmd_folder = os.path.realpath(
    os.path.abspath(
        os.path.split( inspect.getfile( inspect.currentframe() ) )[0]
    ) )
if cmd_folder not in sys.path:
    sys.path.insert( 0, cmd_folder )
cmd_subfolder = os.path.realpath(
    os.path.abspath(
        os.path.join(
            os.path.split( inspect.getfile( inspect.currentframe() ) )[0],
            "src"
        )
    ) )
if cmd_subfolder not in sys.path:
    sys.path.insert( 0, cmd_subfolder )

print "Importing modules"

# import server module
import connector

# Create the server
print "Starting server"
server = connector.Server()
server.run()


