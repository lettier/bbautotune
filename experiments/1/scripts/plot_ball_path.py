'''

David Lettier (C) 2013.

http://www.lettier.com/

Blender 2.68

This script plots the 3D path/trajectory of the ball.

'''

import os;
import sys;
from os import listdir;
from os.path import isfile, join;
import matplotlib.pyplot as plt;
from mpl_toolkits.mplot3d import Axes3D;

# Ball path experiment data directory.

directory = "../data/";

# Get and sort file names.

experiment_files = [ f for f in listdir( directory ) if isfile( join( directory, f ) ) ];

if ( len( experiment_files ) == 0 ):
	
	print( "\nNo files.\n" );
	
	sys.exit( 0 );

# Y_M_D_H_M_S.N-N#0,0#.csv
# 0         5

experiment_files = sorted( experiment_files, key = lambda x: int( "".join( x.split( "_" )[ 0 : 5 ] ) ) );

# List files.

print( "\nFiles: " );

i = 0;

for experiment_file in experiment_files:
	
	print ( "[" + str( i ) + "] " + experiment_file );
	
	i += 1;
	
user_input = raw_input( "\nPlot which file ([q] to quit or [a] for all)?\n" );

# Quit?

if ( user_input[ 0 ] == "q" ):
	
	sys.exit( 0 );
	
# Generate plot setup.

matplotlib_colors = [ "b", "g", "r", "c", "m", "y", "k" ];
matplotlib_colors_index = 0;

fig = plt.figure( figsize = ( 5 * 3.13, 5 * 3.13 ) );
fig.suptitle( "BBAutoTune", fontsize = 18 );

ax = fig.gca( projection = "3d" );
ax.set_title( "Parameter Influence" );
ax.set_xlabel( "x-axis" );
ax.set_ylabel( "y-axis" );
ax.set_zlabel( "z-axis" );
		
# Plot all?
		
if ( user_input[ 0 ] == "a" ):
	
	i = 0;
	
	while ( len( experiment_files ) != 0 ):
		
		# Open files.

		csv_file = None;

		try:
			
			csv_file = open( directory + experiment_files[ i ], "r" );
			
		except:
			
			print( "File does not exist: [" + str( i ) + "] " + directory + experiment_files[ i ] );
			
			sys.exit( 1 );
			
		# Gather points.
			
		x_points = [ ];
		y_points = [ ];
		z_points = [ ];

		titles = csv_file.readline( );

		line = csv_file.readline( );

		while ( line != "" ):
			
			line = line.rstrip( '\n' );
			
			line = line.rsplit( "," );
			
			x_points.append( float( line[ 1 ] ) );
			y_points.append( float( line[ 2 ] ) );
			z_points.append( float( line[ 3 ] ) );
			
			line = csv_file.readline( );
			
		# Create plot label.
			
		# Y_M_D_H_M_S.N-N#0,0#.csv
		# 0           1       2

		# N-N-N#0,0#
		# 0 	   1   2

		# 0,0
		# 0 1

		label = experiment_files[ i ].split( "." )[ 1 ];

		parameter_name = " ".join( label.split( "#" )[ 0 ].split( "-" ) );

		parameter_value = ".".join( label.split( "#" )[ 1 ].split( "," ) );

		label = parameter_name + ": " + parameter_value;
		
		# Add points to plot.

		ax.plot( x_points, y_points, z_points, matplotlib_colors[ matplotlib_colors_index ] + "o-", label = label );
		
		# Remove file from available choices.
		
		del experiment_files[ i ];
		
		if ( len( experiment_files ) == 0 ):
			
			break;
			
		# Use next available color.

		matplotlib_colors_index += 1;
		matplotlib_colors_index = matplotlib_colors_index % len( matplotlib_colors );
		
else: # Plot one by one.	
	
	# Check user input.
	
	while ( True ):

		try:

			user_input = int( user_input );
			
			if ( user_input > ( i - 1 ) ):
				
				user_input = raw_input( "\nPlot which file ([q] to quit)?\n" );
				
				if ( user_input[ 0 ] == "q" ):
					
					break;
					
					sys.exit( 0 );

				continue;
			
			break;
			
		except:
			
			user_input = raw_input( "\nPlot which file ([q] to quit)?\n" );
			
			if ( user_input[ 0 ] == "q" ):
		
				sys.exit( 0 );
			
			continue;

	# Open file.

	csv_file = None;

	try:
		
		csv_file = open( directory + experiment_files[ user_input ], "r" );
		
	except:
		
		print( "File does not exist: [" + str( user_input ) + "] " + directory + experiment_files[ user_input ] );
		
		sys.exit( 1 );
		
	# Read in points.
		
	x_points = [ ];
	y_points = [ ];
	z_points = [ ];

	titles = csv_file.readline( );

	line = csv_file.readline( );

	while ( line != "" ):
		
		line = line.rstrip( '\n' );
		
		line = line.rsplit( "," );
		
		x_points.append( float( line[ 1 ] ) );
		y_points.append( float( line[ 2 ] ) );
		z_points.append( float( line[ 3 ] ) );
		
		line = csv_file.readline( );
		
	# Create plot label.

	# Y_M_D_H_M_S.N-N#0,0#.csv
	# 0           1       2

	# N-N-N#0,0#
	# 0 	   1   2

	# 0,0
	# 0 1

	label = experiment_files[ user_input ].split( "." )[ 1 ];

	parameter_name = " ".join( label.split( "#" )[ 0 ].split( "-" ) );

	parameter_value = ".".join( label.split( "#" )[ 1 ].split( "," ) );

	label = parameter_name + ": " + parameter_value;
	
	# Add points to plot.

	ax.plot( x_points, y_points, z_points, matplotlib_colors[ matplotlib_colors_index ] + "o-", label = label );
	
	# Remove file from possible options.

	del experiment_files[ user_input ];
	
	# Use next available color.

	matplotlib_colors_index += 1;
	matplotlib_colors_index = matplotlib_colors_index % len( matplotlib_colors );

	# Plot multiple paths if there are more than one file?

	if ( len( experiment_files ) == 0 ):
		
		user_input = "0";
		
	else:

		user_input = raw_input( "\nPlot another file?\n[y] Yes.\n[n] No.\n" );

	while ( user_input[ 0 ] == 'y' ):
		
		i = 0;
		
		# List files.
		
		print( "\nFiles: " );
		
		for experiment_file in experiment_files:
		
			print ( "[" + str( i ) + "] " + experiment_file );
			
			i += 1;
		
		user_input = raw_input( "\nPlot which file?\n" );
		
		# Check user input.
		
		while ( True ):

			try:

				user_input = int( user_input );
				
				if ( user_input > ( i - 1 ) ):
					
					user_input = raw_input( "\nPlot which file?\n" );
					
					continue;
				
				break;
				
			except:
				
				user_input = raw_input( "\nPlot which file?\n" );
				
				continue;
		
		# Open file.

		csv_file = None;

		try:
			
			csv_file = open( directory + experiment_files[ user_input ], "r" );
			
		except:
			
			print( "File does not exist: [" + str( user_input ) + "] " + directory + experiment_files[ user_input ] );
			
			sys.exit( 1 );
			
		# Read in points.
			
		x_points = [ ];
		y_points = [ ];
		z_points = [ ];

		titles = csv_file.readline( );

		line = csv_file.readline( );

		while ( line != "" ):
			
			line = line.rstrip( '\n' );
			
			line = line.rsplit( "," );
			
			x_points.append( float( line[ 1 ] ) );
			y_points.append( float( line[ 2 ] ) );
			z_points.append( float( line[ 3 ] ) );
			
			line = csv_file.readline( );
			
		# Create plot label.
			
		# Y_M_D_H_M_S.N-N#0,0#.csv
		# 0           1       2

		# N-N-N#0,0#
		# 0 	   1   2

		# 0,0
		# 0 1

		label = experiment_files[ user_input ].split( "." )[ 1 ];

		parameter_name = " ".join( label.split( "#" )[ 0 ].split( "-" ) );

		parameter_value = ".".join( label.split( "#" )[ 1 ].split( "," ) );

		label = parameter_name + ": " + parameter_value;
		
		# Add points to plot.

		ax.plot( x_points, y_points, z_points, matplotlib_colors[ matplotlib_colors_index ] + "o-", label = label );
		
		# Remove file from possible options.
		
		del experiment_files[ user_input ];
		
		if ( len( experiment_files ) == 0 ):
			
			break;
			
		# Use next available color.

		matplotlib_colors_index += 1;
		matplotlib_colors_index = matplotlib_colors_index % len( matplotlib_colors );
		
		# Plot another file?
		
		user_input = raw_input( "\nPlot another file?\n[y] Yes.\n[n] No.\n" );
	
# Show plot(s).

ax.legend( );
plt.tight_layout( );
plt.subplots_adjust( left = 0.0, right = 1.0, top = 1.0, bottom = 0.0 );
plt.show( );