#!/usr/bin/env python2
##
############
##
## Software under MIT licence
##
############

import socket
import Queue, threading, sys, select

import catch_yt as yt
import processing

class Server:
    def __init__( self ):
        # Host Name
        self.h_name = ''

        # Host Port
        self.h_port = 36326

        # Clients box
        self.clients = []
    
    # Create server socket
    def open_socket( self ):
        try:
            # Create a new socket
            self.server = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
                )

            # Tell to the socket where to listen
            self.server.bind( ( self.h_name, self.h_port ) )

            # Start listening
            self.server.listen( 5 )
            self.clients.append( self.server )
        # Handle error if any
        except socket.error, ( value, message ):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit( 1 )

    def run( self ):
        print "Starting Sockets..."
        # Initialize server connection
        self.open_socket()
        
        try:
            # Endless loop to catch connections
            while True:
                print "\nReady for new connections...\n"
                
                # Wait for connections
                read_sockets, write_sockets, error_sockets = select.select(
                    [self.server],[],[]
                    )
                    
                # Handle connection
                for client in read_sockets:
                    if client == self.server:
                        cli, addr = self.server.accept()
                        print "Connecting client %s:%s" % addr
                        c = Client( ( cli, addr ) )
                        c.start()
                        self.clients.append( c )
                    else:
                        print "Google cares!"
        # Safe ending
        finally:
            print "Exiting..."
            # Close server socket
            self.server.close()
            # Waiting for clients to disconnect
            for client in self.clients:
                client.join()
            sys.exit(0)

# Client events manager object
class Client( threading.Thread ):
    def __init__( self, ( client, address ) ):
        threading.Thread.__init__( self )
        
        # Client socket
        self.client = client
        # Client address
        self.address = address
        
        # Video / Audio service to use
        self.service = None
        # URL to use
        self.url = None
        # Playback settings
        self.opt = None
        # Chunk
        self.chunk = None
        
        # YoutubeCatcher Object
        self.yt = yt.Yt()

    def run( self ):
        ## TODO: make it modular/query-response
        try:
            # (Future feature: multi service) Ask for which service we will work
            self.service = self.client.recv( 16 )
            
            # Ask for url
            self.client.sendall( 'u' )
            self.url = self.client.recv( 1024 )
            self.yt.get_info( self.url )
            
            # Get and send available formats
            data = self.yt.get_format_string()
            self.client.sendall( data )
            formt = self.client.recv(32)
            
            if formt != "":
                # Ask for settings
                self.client.sendall('s')
                self.opt = self.client.recv(4096)
                if self.opt != '{ok}':
                    print "Do Something"
                # Start to stream
                print "Sending %s to %s:%s" % ( self.yt.get_title(), self.address[0], self.address[1] )
                step = 0
                while data != "EOS":
                    step += 1
                    data = self.yt.get_audio( step = step, format = formt )
                    self.client.sendall( data )
        # Safe ending
        finally:
            print "Stopping for %s:%s" % self.address
            self.client.close()
 


