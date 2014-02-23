'''

David Lettier (C) 2014.

http://www.lettier.com/

Records the robot's position and orientation.

'''

import time;
import math;

# Get the controller.

controller = bge.logic.getCurrentController( );

# Get the game object that the controller is attached to.

obj = controller.owner;

# Initialize this script.
# BGE scripts are stateless so save information in the global dictionary.

if ( obj[ "init" ] == False ):
	
	obj[ "init" ] = True;
	
	# X being the simulated robot's position and heading before being given a command.
	
	bge.logic.globalDict[ "X" ] = { 
		
		"x":   bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.x,
		"y":   bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.y,
		"z":   bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.z,
		"t": ( bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).z * ( 180.0 / math.pi ) ) % 360.0
		
	};
	
	bge.logic.globalDict[ "time_start" ] = int( round( time.time( ) * 1000 ) );
	
if ( ( int( round( time.time( ) * 1000 ) ) - bge.logic.globalDict[ "time_start" ] ) <= 1000 ):
	
	# Ending the game engine does not stop the engine immediately.
	# Thus, keep recording the current position until the time
	# elapsed has been 0.5 seconds at which the last recorded position
	# will be the final post position.
	
	# X' being the simulated robot's position and heading after performing a given command.
	
	bge.logic.globalDict[ "X_prime" ] = { 
		
		"x":   bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.x,
		"y":   bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.y,
		"z":   bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.z,
		"t": ( bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).z * ( 180.0 / math.pi ) ) % 360.0
		
	};
	
	shared_data_file_name = obj[ "shared_data_file_name" ];
	
	shared_data_file = open( shared_data_file_name, "w" );
	
	x = str( bge.logic.globalDict[ "X" ][ "x" ] );
	y = str( bge.logic.globalDict[ "X" ][ "y" ] );
	z = str( bge.logic.globalDict[ "X" ][ "z" ] );
	t = str( bge.logic.globalDict[ "X" ][ "t" ] );
	
	shared_data_file.write( x + "," + y + "," + z + "," + t + "\n" );
	
	x = str( bge.logic.globalDict[ "X_prime" ][ "x" ] );
	y = str( bge.logic.globalDict[ "X_prime" ][ "y" ] );
	z = str( bge.logic.globalDict[ "X_prime" ][ "z" ] );
	t = str( bge.logic.globalDict[ "X_prime" ][ "t" ] );
	
	shared_data_file.write( x + "," + y + "," + z + "," + t + "\n" );
	
	shared_data_file.close( );
	
else:
	
	# Send the signal to shut down the game engine.
	
	bge.logic.endGame( );