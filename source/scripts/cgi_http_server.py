#!/usr/bin/env python

'''

David Lettier (C) 2014.

http://www.lettier.com/

Starts a CGI HTTP server that displays the genetic algorithm progress at index.py.

'''
 
import BaseHTTPServer
import CGIHTTPServer
import cgitb; cgitb.enable( );  # This line enables CGI error reporting
import sys;
import thread;
import webbrowser;
import os;

print( "\nCGI HTTP Server | BBAutoTune\n" );

# Set server parameters.
 
server                  = BaseHTTPServer.HTTPServer;
handler                 = CGIHTTPServer.CGIHTTPRequestHandler;
server_address          = ( "", 8000 );

# Change directory to the scripts directory.

current_working_directory = os.getcwd( );
		
current_working_directory = current_working_directory.rsplit( "/", 1 )

while ( current_working_directory[ 1 ] != "bbautotune" ):
	
	current_working_directory = current_working_directory[ 0 ].rsplit( "/", 1 );

os.chdir( current_working_directory[ 0 ] + "/bbautotune/source/scripts/" );

# Set the server directories.

handler.cgi_directories = [ "/", "/" ];

# Create the server.
 
httpd = server( server_address, handler );

# Run the server function.

def run_server( ):
	
	print( "Server started.\nServing To: http://localhost:8000\n" );
	
	httpd.serve_forever( );
	
# Run the server in a thread.
	
thread.start_new_thread( run_server, ( ) );

# Process command line arguments.
# -w indicates to open the web browser to index.py.

if ( len( sys.argv ) == 2 ):
	
	if ( sys.argv[ 1 ] == "-w" ):

		index_url = "http://localhost:8000/index.py";

		print( "Opening web browser. One moment.\n" );

		webbrowser.open_new_tab( index_url );
	
# Listen for q to shutdown the server.

quit = "";

while not ( quit == "q" ):

	quit = raw_input( "Type [q] to quit.\n" );
	
print( "Exiting the server.\n" );
	
sys.exit( 0 );