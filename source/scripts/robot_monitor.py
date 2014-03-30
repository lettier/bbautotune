'''

David Lettier (C) 2014.

http://www.lettier.com/

Records the robot's position and orientation.

'''

import time;
import math;

# Handles the initial and the final states of the robot.

def handle_initial_and_final_states( ):
	
	# Initial being the simulated robot's 6dof after performing a command.
	# Final will be updated until the robot stops moving or after 16 seconds--whatever comes first.
	# The last Final recorded will be the Final evaluated.
		
	bge.logic.globalDict[ "Final" ] = { 
		
		"x_pos": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.x * 100.0, # In centimeters.
		"y_pos": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.y * 100.0, # In centimeters.
		"z_pos": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.z * 100.0, # In centimeters.
		"x_ori": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).x, # In radians.
		"y_ori": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).y, # In radians.
		"z_ori": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).z  # In radians.
		
	};

	# Send to Blender debug properties.

	obj[ "x'_pos" ] = "%10.6f" % bge.logic.globalDict[ "Final" ][ "x_pos" ];
	obj[ "y'_pos" ] = "%10.6f" % bge.logic.globalDict[ "Final" ][ "y_pos" ];
	obj[ "z'_pos" ] = "%10.6f" % bge.logic.globalDict[ "Final" ][ "z_pos" ];
	obj[ "x'_ori" ] = "%10.6f" % bge.logic.globalDict[ "Final" ][ "x_ori" ];
	obj[ "y'_ori" ] = "%10.6f" % bge.logic.globalDict[ "Final" ][ "y_ori" ];
	obj[ "z'_ori" ] = "%10.6f" % bge.logic.globalDict[ "Final" ][ "z_ori" ];

	shared_data_file_name = obj[ "shared_data_file_name" ];

	shared_data_file = open( shared_data_file_name, "w" );

	x_initial_pos = str( bge.logic.globalDict[ "Initial" ][ "x_pos" ] );
	y_initial_pos = str( bge.logic.globalDict[ "Initial" ][ "y_pos" ] );
	z_initial_pos = str( bge.logic.globalDict[ "Initial" ][ "z_pos" ] );
	x_initial_ori = str( bge.logic.globalDict[ "Initial" ][ "x_ori" ] );
	y_initial_ori = str( bge.logic.globalDict[ "Initial" ][ "y_ori" ] );
	z_initial_ori = str( bge.logic.globalDict[ "Initial" ][ "z_ori" ] );
	s_initial_tim = str( bge.logic.globalDict[ "time_start" ] );	

	shared_data_file.write( x_initial_pos + "," + y_initial_pos + "," + z_initial_pos + "," + x_initial_ori + "," + y_initial_ori + "," + z_initial_ori + "," + s_initial_tim + "\n" );

	x_final_pos = str( bge.logic.globalDict[ "Final" ][ "x_pos" ] );
	y_final_pos = str( bge.logic.globalDict[ "Final" ][ "y_pos" ] );
	z_final_pos = str( bge.logic.globalDict[ "Final" ][ "z_pos" ] );
	x_final_ori = str( bge.logic.globalDict[ "Final" ][ "x_ori" ] );
	y_final_ori = str( bge.logic.globalDict[ "Final" ][ "y_ori" ] );
	z_final_ori = str( bge.logic.globalDict[ "Final" ][ "z_ori" ] );
	e_final_tim = str( time.time( ) * 1000.0 );

	shared_data_file.write( x_final_pos + "," + y_final_pos + "," + z_final_pos + "," + x_final_ori + "," + y_final_ori + "," + z_final_ori + "," + e_final_tim + "\n" );

	shared_data_file.close( );

# Get the controller.

controller = bge.logic.getCurrentController( );

# Get the game object that the controller is attached to.

obj = controller.owner;

# Initialize this script.
# BGE scripts are stateless so save information in the global dictionary.

if ( obj[ "init" ] == False ):
	
	obj[ "init" ] = True;
	
	# Check time in milliseconds.
	
	bge.logic.globalDict[ "check_time" ] = 1000.0;
	
	# Initial being the simulated robot's 6dof before performing a command.
	
	# Blender implicitly reports positions in meters.
	# However the real robot data was reported in centimeters.
	# Thus, convert the reading in meters to centimeters.
	# 1.0m = 100.00cm
	
	bge.logic.globalDict[ "Initial" ] = { 
		
		"x_pos": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.x * 100.0, # In centimeters.
		"y_pos": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.y * 100.0, # In centimeters.
		"z_pos": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.z * 100.0, # In centimeters.
		"x_ori": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).x, # In radians.
		"y_ori": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).y, # In radians.
		"z_ori": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).z  # In radians.
		
	};
	
	# Send to Blender debug properties.
	
	obj[ "x_pos" ] = "%10.6f" % bge.logic.globalDict[ "Initial" ][ "x_pos" ];
	obj[ "y_pos" ] = "%10.6f" % bge.logic.globalDict[ "Initial" ][ "y_pos" ];
	obj[ "z_pos" ] = "%10.6f" % bge.logic.globalDict[ "Initial" ][ "z_pos" ];
	obj[ "x_ori" ] = "%10.6f" % bge.logic.globalDict[ "Initial" ][ "x_ori" ];
	obj[ "y_ori" ] = "%10.6f" % bge.logic.globalDict[ "Initial" ][ "y_ori" ];
	obj[ "z_ori" ] = "%10.6f" % bge.logic.globalDict[ "Initial" ][ "z_ori" ];
	
	# Start time of evaluation.
	
	bge.logic.globalDict[ "time_start" ] = time.time( ) * 1000.0;
	
# Report current running evaluation time to Blender debug properties.

obj[ "elapsed_time" ] = ( ( time.time( ) * 1000.0 ) - bge.logic.globalDict[ "time_start" ] );
	
# After one second and after every half second after that check if the robot has stopped.
	
if ( ( ( time.time( ) * 1000.0 ) - bge.logic.globalDict[ "time_start" ] ) >= bge.logic.globalDict[ "check_time" ] ):
	
	stopped_test = { 
		
		"x_pos": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.x * 100.0, # In centimeters.
		"y_pos": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.y * 100.0, # In centimeters.
		"z_pos": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldPosition.z * 100.0, # In centimeters.
		"x_ori": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).x, # In radians.
		"y_ori": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).y, # In radians.
		"z_ori": bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].worldOrientation.to_euler( ).z  # In radians.
		
	};
	
	still_moving = len( set( bge.logic.globalDict[ "Final" ].items( ) ) ^ set( stopped_test.items( ) ) );
	
	if ( still_moving != 0 ):
		
		bge.logic.globalDict[ "check_time" ] += 500.0
		
	else:
		
		bge.logic.endGame( );
		
handle_initial_and_final_states( );

# Stop evaluation after 16 seconds.

if ( ( time.time( ) * 1000.0 ) - bge.logic.globalDict[ "time_start" ] >= 16000 ):
	
	bge.logic.endGame( );