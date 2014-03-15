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
	
	# P being the simulated robot's position and heading before performing a command.
	
	# Blender implicity reports positions in meters.
	# However the real robot data was reported in centimeters.
	# Thus convert the reading in meters to centimeters.
	# 1.0m = 100.00cm
	
	bge.logic.globalDict[ "P" ] = { 
		
		"x": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.x * 100.0,
		"y": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.y * 100.0,
		"z": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.z * 100.0,
		"t": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).z # In radians.
		
	};
	
	# Send to Blender debug properties.
	
	obj[ "x" ] = "%.6f" % bge.logic.globalDict[ "P" ][ "x" ];
	obj[ "y" ] = "%.6f" % bge.logic.globalDict[ "P" ][ "y" ];
	obj[ "z" ] = "%.6f" % bge.logic.globalDict[ "P" ][ "z" ];
	obj[ "t" ] = "%.6f" % bge.logic.globalDict[ "P" ][ "t" ];
	
	# Start time of evaluation.
	
	bge.logic.globalDict[ "time_start" ] = time.time( );
	
if ( ( time.time( ) - bge.logic.globalDict[ "time_start" ] ) <= 2.0 ):
	
	# Ending the game engine does not stop the engine immediately.
	# Thus, keep recording the current position until the time
	# elapsed has been 2 seconds at which the last recorded position
	# will be the final post position.
	
	# P' being the simulated robot's position and heading after performing a command.
	
	bge.logic.globalDict[ "P_prime" ] = { 
		
		"x": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.x * 100.0,
		"y": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.y * 100.0,
		"z": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.z * 100.0,
		"t": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).z # In radians.
		
	};
	
	# Send to Blender debug properties.
	
	obj[ "x'" ] = "%.6f" % bge.logic.globalDict[ "P_prime" ][ "x" ];
	obj[ "y'" ] = "%.6f" % bge.logic.globalDict[ "P_prime" ][ "y" ];
	obj[ "z'" ] = "%.6f" % bge.logic.globalDict[ "P_prime" ][ "z" ];
	obj[ "t'" ] = "%.6f" % bge.logic.globalDict[ "P_prime" ][ "t" ];
	
	shared_data_file_name = obj[ "shared_data_file_name" ];
	
	shared_data_file = open( shared_data_file_name, "w" );
	
	x = str( bge.logic.globalDict[ "P" ][ "x" ] );
	y = str( bge.logic.globalDict[ "P" ][ "y" ] );
	z = str( bge.logic.globalDict[ "P" ][ "z" ] );
	t = str( bge.logic.globalDict[ "P" ][ "t" ] );
	
	shared_data_file.write( x + "," + y + "," + z + "," + t + "\n" );
	
	x_prime = str( bge.logic.globalDict[ "P_prime" ][ "x" ] );
	y_prime = str( bge.logic.globalDict[ "P_prime" ][ "y" ] );
	z_prime = str( bge.logic.globalDict[ "P_prime" ][ "z" ] );
	t_prime = str( bge.logic.globalDict[ "P_prime" ][ "t" ] );
	
	shared_data_file.write( x_prime + "," + y_prime + "," + z_prime + "," + t_prime + "\n" );
	
	shared_data_file.close( );
	
else:
	
	# Send the signal to shut down the game engine.
	
	bge.logic.endGame( );
	
# Report current running evaluation time to Blender debug properties.

obj[ "time" ] = ( time.time( ) - bge.logic.globalDict[ "time_start" ] );