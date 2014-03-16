'''

David Lettier (C) 2014.

http://www.lettier.com/

Records the robot's position and orientation.

'''

import time;
import math;

# Handles P and P'.

def handle_p_and_p_prime( ):
	
	# P' being the simulated robot's 6dof after performing a command.
	# P' will be updated until the robot stops moving or after 10 seconds--whatever comes first.
	# The last P' recorded will be the P' evaluated.
		
	bge.logic.globalDict[ "P_prime" ] = { 
		
		"x_pos": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.x * 100.0, # In centimeters.
		"y_pos": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.y * 100.0, # In centimeters.
		"z_pos": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.z * 100.0, # In centimeters.
		"x_ori": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).x, # In radians.
		"y_ori": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).y, # In radians.
		"z_ori": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).z  # In radians.
		
	};

	# Send to Blender debug properties.

	obj[ "x'_pos" ] = "%10.6f" % bge.logic.globalDict[ "P_prime" ][ "x_pos" ];
	obj[ "y'_pos" ] = "%10.6f" % bge.logic.globalDict[ "P_prime" ][ "y_pos" ];
	obj[ "z'_pos" ] = "%10.6f" % bge.logic.globalDict[ "P_prime" ][ "z_pos" ];
	obj[ "x'_ori" ] = "%10.6f" % bge.logic.globalDict[ "P_prime" ][ "x_ori" ];
	obj[ "y'_ori" ] = "%10.6f" % bge.logic.globalDict[ "P_prime" ][ "y_ori" ];
	obj[ "z'_ori" ] = "%10.6f" % bge.logic.globalDict[ "P_prime" ][ "z_ori" ];

	shared_data_file_name = obj[ "shared_data_file_name" ];

	shared_data_file = open( shared_data_file_name, "w" );

	x_pos = str( bge.logic.globalDict[ "P" ][ "x_pos" ] );
	y_pos = str( bge.logic.globalDict[ "P" ][ "y_pos" ] );
	z_pos = str( bge.logic.globalDict[ "P" ][ "z_pos" ] );
	x_ori = str( bge.logic.globalDict[ "P" ][ "x_ori" ] );
	y_ori = str( bge.logic.globalDict[ "P" ][ "y_ori" ] );
	z_ori = str( bge.logic.globalDict[ "P" ][ "z_ori" ] );
	s_tim = str( bge.logic.globalDict[ "time_start" ] );
	

	shared_data_file.write( x_pos + "," + y_pos + "," + z_pos + "," + x_ori + "," + y_ori + "," + z_ori + "," + s_tim + "\n" );

	x_prime_pos = str( bge.logic.globalDict[ "P_prime" ][ "x_pos" ] );
	y_prime_pos = str( bge.logic.globalDict[ "P_prime" ][ "y_pos" ] );
	z_prime_pos = str( bge.logic.globalDict[ "P_prime" ][ "z_pos" ] );
	x_prime_ori = str( bge.logic.globalDict[ "P_prime" ][ "x_ori" ] );
	y_prime_ori = str( bge.logic.globalDict[ "P_prime" ][ "y_ori" ] );
	z_prime_ori = str( bge.logic.globalDict[ "P_prime" ][ "z_ori" ] );
	e_prime_tim = str( time.time( ) * 1000.0 );

	shared_data_file.write( x_prime_pos + "," + y_prime_pos + "," + z_prime_pos + "," + x_prime_ori + "," + y_prime_ori + "," + z_prime_ori + "," + e_prime_tim + "\n" );

	shared_data_file.close( );

# Get the controller.

controller = bge.logic.getCurrentController( );

# Get the game object that the controller is attached to.

obj = controller.owner;

# Initialize this script.
# BGE scripts are stateless so save information in the global dictionary.

if ( obj[ "init" ] == False ):
	
	obj[ "init" ] = True;
	
	# Check time in miliseconds.
	
	bge.logic.globalDict[ "check_time" ] = 1000.0;
	
	# P being the simulated robot's 6dof before performing a command.
	
	# Blender implicity reports positions in meters.
	# However the real robot data was reported in centimeters.
	# Thus convert the reading in meters to centimeters.
	# 1.0m = 100.00cm
	
	bge.logic.globalDict[ "P" ] = { 
		
		"x_pos": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.x * 100.0, # In centimeters.
		"y_pos": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.y * 100.0, # In centimeters.
		"z_pos": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.z * 100.0, # In centimeters.
		"x_ori": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).x, # In radians.
		"y_ori": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).y, # In radians.
		"z_ori": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).z  # In radians.
		
	};
	
	# Send to Blender debug properties.
	
	obj[ "x_pos" ] = "%10.6f" % bge.logic.globalDict[ "P" ][ "x_pos" ];
	obj[ "y_pos" ] = "%10.6f" % bge.logic.globalDict[ "P" ][ "y_pos" ];
	obj[ "z_pos" ] = "%10.6f" % bge.logic.globalDict[ "P" ][ "z_pos" ];
	obj[ "x_ori" ] = "%10.6f" % bge.logic.globalDict[ "P" ][ "x_ori" ];
	obj[ "y_ori" ] = "%10.6f" % bge.logic.globalDict[ "P" ][ "y_ori" ];
	obj[ "z_ori" ] = "%10.6f" % bge.logic.globalDict[ "P" ][ "z_ori" ];
	
	# Start time of evaluation.
	
	bge.logic.globalDict[ "time_start" ] = time.time( ) * 1000.0;
	
# Report current running evaluation time to Blender debug properties.

obj[ "elapsed_time" ] = ( ( time.time( ) * 1000.0 ) - bge.logic.globalDict[ "time_start" ] );
	
# After one second, check if the robot has moved every half second.
	
if ( ( ( time.time( ) * 1000.0 ) - bge.logic.globalDict[ "time_start" ] ) >= bge.logic.globalDict[ "check_time" ] ):
	
	p_prime_test = { 
		
		"x_pos": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.x * 100.0, # In centimeters.
		"y_pos": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.y * 100.0, # In centimeters.
		"z_pos": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.z * 100.0, # In centimeters.
		"x_ori": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).x, # In radians.
		"y_ori": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).y, # In radians.
		"z_ori": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).z  # In radians.
		
	};
	
	still_moving = len( set( bge.logic.globalDict[ "P_prime" ].items( ) ) ^ set( p_prime_test.items( ) ) );
	
	if ( still_moving != 0 ):
		
		bge.logic.globalDict[ "check_time" ] += 500.0
		
	else:
		
		bge.logic.endGame( );
		
handle_p_and_p_prime( );

# Stop evaluation after 16 seconds.

if ( ( time.time( ) * 1000.0 ) - bge.logic.globalDict[ "time_start" ] >= 16000 ):
	
	bge.logic.endGame( );
