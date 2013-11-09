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
	
	directory = directory + "experiment_data/1/";
	
	time_stamp = datetime.datetime.fromtimestamp( time.time( ) ).strftime( "%Y_%m_%d_%H_%M_%S" );
	
	milliseconds = str( int( round( time.time( ) * 1000 ) ) );
	
	csv_file = open( directory + time_stamp + ".csv", "w" );
	
	ball[ "file_path" ] = directory + time_stamp + ".csv";
	
	csv_file.write( "'milliseconds','x','y','z'\n" );
	
	csv_file.write( "" + milliseconds + "," + str( ball.worldPosition.x ) + "," + str( ball.worldPosition.y ) + "," + str( ball.worldPosition.z ) + "\n" );
	
	csv_file.close( );
	
	ball[ "init_file" ] = False;
	
else:
	
	csv_file = open( ball[ "file_path" ], "a" );
	
	milliseconds = str( int( round( time.time( ) * 1000 ) ) );

	csv_file.write( "" + milliseconds + "," + str( ball.worldPosition.x ) + "," + str( ball.worldPosition.y ) + "," + str( ball.worldPosition.z ) + "\n" );
		
	csv_file.close( );



