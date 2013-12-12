'''

David Lettier (C) 2013.

http://www.lettier.com/

This script calculates the Lettier Distance, the Frechet Distance, and the Hausdorff Distance
between the standard ball's trajectory (P) and any tweaked parameter ball's trajectory (Q).

'''

import os;
import sys;
from os import listdir;
from os.path import isfile, join;
import math;

def Lettier_Distance( P, Q ):

	'''
	
	Imagine you have a rubber band connected to the two starting point positions 
	in both P and Q. At each step, you advance one end of the rubber band to the 
	next point in P and the other end of the rubber band to the next point in Q. 
	If the distance grows between points Pi and Qi, the rubber band stretches but
	never shrinks. The resulting length of the rubber band is the max Euclidean 
	distance once you reach Pn and Qn.
	
	If |P| < |Q| then keep advancing through the points in Q while keeping the one
	end of the rubber band fixed at the last point in P.
	
	If |P| > |Q| then keep advancing through the points in P while keeping the one
	end of the rubber band fixed at the last point in Q.
	
	''' 

	max_distance = 0.0;
	
	i = 0;
	
	for Pi in P:
	
		Qi = None;
	
		try:
	
			Qi = Q[ i ];
			
		except IndexError:
		
			# |P| > |Q|
			
			i = i - 1;
			
			# Last point in Q.
			
			Qi = Q[ i ];
		
		delta_x = Qi[ 0 ] - Pi[ 0 ];
		delta_y = Qi[ 1 ] - Pi[ 1 ];
		delta_z = Qi[ 2 ] - Pi[ 2 ];
	
		distance = math.sqrt( math.pow( delta_x, 2 ) + math.pow( delta_y, 2 ) + math.pow( delta_z, 2 ) );
		
		if max_distance < distance:
		
			max_distance = distance;
		
		i = i + 1;
		
	# i = |P| - 1
		
	i = i - 1;
	
	# Last point index in P.
		
	j = i;
		
	if i != len( Q ) - 1:
	
		# |P| < |Q|
	
		# Last point in P.
	
		Pi = P[ j ];
		
		for k in xrange( i + 1, len( Q ) ):
		
			# Keep advancing through Q.
		
			Qi = Q[ k ];
		
			delta_x = Qi[ 0 ] - Pi[ 0 ];
			delta_y = Qi[ 1 ] - Pi[ 1 ];
			delta_z = Qi[ 2 ] - Pi[ 2 ];
	
			distance = math.sqrt( math.pow( delta_x, 2 ) + math.pow( delta_y, 2 ) + math.pow( delta_z, 2 ) );
		
			if max_distance < distance:
		
				max_distance = distance;
		
	return max_distance;
	
def Frechet_Distance( P, Q ):

	distance_matrix_PxQ = [ ];
	
	for Pi in P:
	
		Pi_distances = [ ];
		
		for Qi in Q:
		
			delta_x = Qi[ 0 ] - Pi[ 0 ];
			delta_y = Qi[ 1 ] - Pi[ 1 ];
			delta_z = Qi[ 2 ] - Pi[ 2 ];
	
			distance = math.sqrt( math.pow( delta_x, 2 ) + math.pow( delta_y, 2 ) + math.pow( delta_z, 2 ) );
			
			Pi_distances.append( distance );
			
		distance_matrix_PxQ.append( Pi_distances );

	i = 0;
	j = 0;
	
	max_distance = 0.0;
	
	while True:
	
		if ( i == len( P ) - 1 ) and ( j == len( Q ) - 1 ):
		
			break;
			
		elif i == len( P ) - 1: # i is all the way down the matrix.
		
			# You can only go to the right in the matrix.
		
			right_distance = distance_matrix_PxQ[ i     ][ j + 1 ];
			
			if max_distance < right_distance:
			
				max_distance = right_distance
			
			j = j + 1;
		
		elif j == len( Q ) - 1: # j is all the way to the right of the matrix.
		
			# You can only go down the matrix.
		
			down_distance = distance_matrix_PxQ[ i + 1 ][ j     ];
			
			if max_distance < down_distance:
			
				max_distance = down_distance
			
			i = i + 1;
		
		else:
		
			diagonal_distance = distance_matrix_PxQ[ i + 1 ][ j + 1 ]; # a
			right_distance    = distance_matrix_PxQ[ i     ][ j + 1 ]; # b
			down_distance     = distance_matrix_PxQ[ i + 1 ][ j     ]; # c
			
			if diagonal_distance <= right_distance: # If a <= b
			
				if diagonal_distance <= down_distance: # If a <= c
				
					# Go diagonal.
					
					if max_distance < diagonal_distance:
					
						max_distance = diagonal_distance
						
					i = i + 1;
					j = j + 1;
					
				else: # c < a
				
					# Go down.
					
					if max_distance < down_distance:
					
						max_distance = down_distance
						
					i = i + 1;
					
			else: # b < a
			
				if right_distance <= down_distance: # If b <= c
				
					# Go right.
					
					if max_distance < right_distance:
					
						max_distance = right_distance
						
					j = j + 1;
					
				else: # c < b
				
					# Go down.
					
					if max_distance < down_distance:
					
						max_distance = down_distance
						
					i = i + 1;
					
	return max_distance;
	
def Hausdorff_Distance( P, Q ):

	def Directed_Hausdorff_Distance( P, Q ):
	
		max_min_distance = 0.0;

		for Pi in P:
		
			min_distance = sys.float_info.max;
			
			for Qi in Q:
			
				delta_x = Qi[ 0 ] - Pi[ 0 ];
				delta_y = Qi[ 1 ] - Pi[ 1 ];
				delta_z = Qi[ 2 ] - Pi[ 2 ];
	
				distance = math.sqrt( math.pow( delta_x, 2 ) + math.pow( delta_y, 2 ) + math.pow( delta_z, 2 ) );
			
				if distance < min_distance:
			
					min_distance = distance;
				
			if min_distance > max_min_distance:
		
				max_min_distance = min_distance;
			
		return max_min_distance;
		
	return max( Directed_Hausdorff_Distance( P, Q ), Directed_Hausdorff_Distance( Q, P ) );

# Ball path experiment data directory.

directory = "../data/";

# Get and sort file names.

experiment_files = [ f for f in listdir( directory ) if isfile( join( directory, f ) ) ];

if ( len( experiment_files ) == 0 ):
	
	print( "\nNo files.\n" );
	
	sys.exit( 0 );
	
# Get rid of the max distances file as one of the files to read in.
	
distances_file_index = 0;

for i in xrange( 0, len( experiment_files ) ):

	if experiment_files[ i ].find( "distances_to_standard" ) != -1:
	
		distances_file_index = i;
		
		break;
		
del experiment_files[ distances_file_index ];

# Y_M_D_H_M_S.N-N#0,0#.csv
# 0         5

experiment_files = sorted( experiment_files, key = lambda x: int( "".join( x.split( "_" )[ 0 : 5 ] ) ) );

standard_file_index = 0;

for i in xrange( 0, len( experiment_files ) ):

	if experiment_files[ i ].find( "Standard" ) != -1:
	
		standard_file_index = i;
		
		break;
		
print "File chosen as the standard: " + experiment_files[ standard_file_index ];

# Open standard file and read in the 3D points.

csv_file = None;

try:
	
	csv_file = open( directory + experiment_files[ standard_file_index ], "r" );
	
except:
	
	print( "File does not exist: " + directory + experiment_files[ standard_file_index ] );
	
	sys.exit( 1 );
	
# Gather points.
	
standard_file_points = [ ];

titles = csv_file.readline( );

line = csv_file.readline( );

while ( line != "" ):
	
	line = line.rstrip( '\n' );
	
	line = line.rsplit( "," );
	
	standard_file_points.append( ( float( line[ 1 ] ), float( line[ 2 ] ), float( line[ 3 ] ) ) );
	
	line = csv_file.readline( );
	
del experiment_files[ standard_file_index ];

distances_to_standard_csv_file = open( directory + "distances_to_standard.csv", "w+" );

distances_to_standard_csv_file.write( ",'Lettier Distance','Frechet Distance','Hausdorff Distance'\n" );

i = 0;

while len( experiment_files ) != 0:

	# Open file and read in the 3D points.

	csv_file = None;

	try:
	
		csv_file = open( directory + experiment_files[ i ], "r" );
	
	except:
	
		print( "File does not exist: " + directory + experiment_files[ i ] );
	
		sys.exit( 1 );
		
	print "Calculating distances for: " + experiment_files[ i ];
	
	# Gather points.
	
	file_points = [ ];

	titles = csv_file.readline( );

	line = csv_file.readline( );

	while ( line != "" ):
	
		line = line.rstrip( '\n' );
	
		line = line.rsplit( "," );
	
		file_points.append( ( float( line[ 1 ] ), float( line[ 2 ] ), float( line[ 3 ] ) ) );
	
		line = csv_file.readline( );

	trajectory_name = experiment_files[ i ].split( "." )[ 1 ];

	parameter_name  = " ".join( trajectory_name.split( "#" )[ 0 ].split( "-" ) );

	parameter_value = ".".join( trajectory_name.split( "#" )[ 1 ].split( "," ) );

	trajectory_name = parameter_name + ": " + parameter_value;
	
	distances_to_standard_csv_file.write( "'" + trajectory_name + "'," );
	
	lettier_distance = Lettier_Distance( standard_file_points, file_points );
	
	frechet_distance = Frechet_Distance( standard_file_points, file_points );
	
	hausdorff_distance = Hausdorff_Distance( standard_file_points, file_points );
	
	distances_to_standard_csv_file.write( str( lettier_distance ) + "," + str( frechet_distance ) + "," + str( hausdorff_distance ) + "\n" );
	
	del experiment_files[ i ];
	
distances_to_standard_csv_file.close( );
