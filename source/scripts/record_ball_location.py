'''

David Lettier (C) 2013.

http://www.lettier.com/

Blender 2.68

This script records the location of the ball and outputs it to a CSV file.

'''

import datetime;
import time;
import os;

controller = bge.logic.getCurrentController( );
ball = controller.owner;

if ball[ "init_file" ] == True:
	
	# Create file.
	
	directory = bge.logic.expandPath( "//" );
	
	directory = directory.replace( "source/blends/", "" );
	
	directory = directory + "experiments/1/data/";
	
	time_stamp = datetime.datetime.fromtimestamp( time.time( ) ).strftime( "%Y_%m_%d_%H_%M_%S" );
	
	milliseconds_start = int( round( time.time( ) * 1000 ) );
	
	ball[ "msecs_start" ] = milliseconds_start;
	
	ball[ "file_path" ] = directory + time_stamp + "." + ball[ "run_name" ] + "." + "csv"
	
	csv_file = open( ball[ "file_path" ], "w" );
	
	csv_file.write( "millisecond,x,y,z," + ball[ "run_name" ] + "\n" );
	
	csv_file.write( "" + str( 0 ) + "," + str( ball.worldPosition.x ) + "," + str( ball.worldPosition.y ) + "," + str( ball.worldPosition.z ) + "\n" );
	
	csv_file.close( );
	
	ball[ "init_file" ] = False;
	
else:
	
	csv_file = open( ball[ "file_path" ], "a" );
	
	milliseconds_delta = ( int( round( time.time( ) * 1000 ) ) ) - ball[ "msecs_start" ];

	csv_file.write( "" + str( milliseconds_delta ) + "," + str( ball.worldPosition.x ) + "," + str( ball.worldPosition.y ) + "," + str( ball.worldPosition.z ) + "\n" );
		
	csv_file.close( );
	
	if ( milliseconds_delta >= 5000 ):
		
		bge.logic.endGame( );