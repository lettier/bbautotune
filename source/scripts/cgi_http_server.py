#!/usr/bin/env python
 
import BaseHTTPServer
import CGIHTTPServer
import cgitb; cgitb.enable( );  # This line enables CGI error reporting
import sys;
import thread;
import webbrowser;
import os;
 
server                  = BaseHTTPServer.HTTPServer;
handler                 = CGIHTTPServer.CGIHTTPRequestHandler;
server_address          = ( "", 8000 );

current_working_directory = os.getcwd( );

print( current_working_directory );

if ( current_working_directory.rsplit( "/", 1 )[ 1 ] == "blends" ):
	
	scripts_location = current_working_directory.rsplit( "/", 1 )[ 0 ] + "/scripts";
	
	os.chdir( scripts_location );

	handler.cgi_directories = [ "/", "/" ];
	
elif ( current_working_directory.rsplit( "/", 1 )[ 1 ] == "source" ):
	
	scripts_location = current_working_directory + "/scripts";
	
	os.chdir( scripts_location );

	handler.cgi_directories = [ "/", "/" ];
	
else:
	
	handler.cgi_directories = [ "/", "/" ];
 
httpd = server( server_address, handler );

def run_server( ):
	
	print( "Server started.\nServing To: http://localhost:8000\n" );
	
	httpd.serve_forever( );
	
thread.start_new_thread( run_server, ( ) );

index_url = "http://localhost:8000/index.py";

print( "\nCGI HTTP Server | BBAutoTune\n" );

print( "Opening web browser. One moment.\n" );

webbrowser.open_new_tab( index_url );

quit = "";

while not ( quit == "q" ):

	quit = raw_input( "Type [q] to quit.\n" );
	
print( "Exiting the server.\n" );
	
sys.exit( 0 );