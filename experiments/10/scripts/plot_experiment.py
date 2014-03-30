'''

David Lettier (C) 2014.

http://www.lettier.com/

Plots a BBAutoTune GA experiment.

'''

import sys;
import numpy as np;
import math;
import pickle;
import matplotlib.pyplot as plt;
import matplotlib.mlab as mlab;
from mpl_toolkits.mplot3d import Axes3D;
from matplotlib import cm;
from matplotlib.patches import Rectangle;
from scipy.stats import scoreatpercentile;
from scipy.stats import normaltest;
from scipy.stats import norm;
from scipy.stats import probplot;
from scipy.stats import mode;

data_file = open( "../data/population_metrics.csv", "r" );

line = data_file.readline( ); # Get rid of the headers.

line = data_file.readline( );

generations = [ ];

highest_fitnesses = [ ];
average_fitnesses = [ ];
lowest_fitnesses  = [ ];

crossover_probabilities = [ ];
mutation_probabilities  = [ ];

line_i = 1;

while line != "":
	
	if ( line[ 0 ] == "#" ):
		
		# Ignore comments.
		
		line    = data_file.readline( );
		line_i += 1;
		
		continue;
	
	splitted = line.split( "," );
	
	g = int( splitted[ 1 ].rstrip( ).strip( '"' ) );
	
	h = float( splitted[ 2 ].rstrip( ).strip( '"' ) );
	a = float( splitted[ 3 ].rstrip( ).strip( '"' ) );
	l = float( splitted[ 4 ].rstrip( ).strip( '"' ) );
	
	c = float( splitted[ 5 ].rstrip( ).strip( '"' ) );
	m = float( splitted[ 6 ].rstrip( ).strip( '"' ) );
	
	generations.append( g );
	
	highest_fitnesses.append( h );
	average_fitnesses.append( a );
	lowest_fitnesses.append( l );
	
	crossover_probabilities.append( c );
	mutation_probabilities.append( m );	
	
	line    = data_file.readline( );
	line_i += 1;

print "Number of lines read: ", line_i;

# Plot high avg low cross mut.

plt.figure( 1 );

plt.subplot( 4, 1, 1 );
plt.plot(  generations, highest_fitnesses, "-b" );
plt.title( "BBAutoTune \n\n Experiment Two \n\n Highest Fitness" );
plt.xlabel( "Generation" );
plt.xticks( np.arange( min( generations ), max( generations ) + 26, 25 ) );
plt.ylabel( "" );
plt.grid( True );

plt.subplot( 4, 1, 2 );
plt.plot( generations, average_fitnesses,"-g" );
plt.title( "Average Fitness" );
plt.xlabel( "Generation" );
plt.ylabel( "" );
plt.xticks( np.arange( min( generations ), max( generations ) + 26, 25 ) );
plt.grid( True );

plt.subplot( 4, 1, 3 );
plt.plot( generations, lowest_fitnesses,"-r" );
plt.title( "Lowest Fitness" );
plt.xlabel( "Generation" );
plt.ylabel( "" );
plt.xticks( np.arange( min( generations ), max( generations ) + 26, 25 ) );
plt.grid( True );

plt.subplot( 4, 1, 4 );
plt.plot( generations, crossover_probabilities,"-b" );
plt.plot( generations, mutation_probabilities, "-g" );
plt.title( "Crossover and Mutation Probability" );
plt.xlabel( "Generation" );
plt.xticks( np.arange( min( generations ), max( generations ) + 26, 25 ) );
plt.yticks( np.arange( 0.0, 1.1, 0.1 ) );
plt.grid( True );

#plt.tight_layout( pad = 1.08, h_pad = 0.5 );

# Rotates a point around the origin, counter-clockwise.

def rotate_point( x, y, angle_r ):
	
	x_rot = ( math.cos( angle_r ) * x ) + ( -math.sin( angle_r ) * y );
	y_rot = ( math.sin( angle_r ) * x ) + (  math.cos( angle_r ) * y );
	
	return x_rot, y_rot;

# Plot the movement of the best and worst performing genomes.

best_initial = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ];
best_final   = [ 23.123499751091003, .009536895231576636, 0.0, 0.0, -0.0, 0.002033736789599061 ];

worst_initial = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ];
worst_final   = [ 34427.630615234375, 1097.4571228027344, 0.0, 0.0, 0.0, -1.9281736612319946 ];

real_robot_centroid = [ 23.8644631679, 0.338269853117, -0.00417473025048 ];

plt.figure( 2 );

plt.title( "BBAutoTune \n\n Experiment Two \n Best and Worst Performing Phenotypes" );
plt.ylabel( "Y-translation" );
plt.xlabel( "X-translation" );
plt.grid( True );
plt.axis( "equal" );

arrow_size = 3.0;

# Plot the worst.

'''

plt.plot( [ worst_initial[ 0 ], worst_final[ 0 ] ], [ worst_initial[ 1 ], worst_final[ 1 ] ], "--r", linewidth = 1 );

plt.plot( [ worst_initial[ 0 ] ], [ worst_initial[ 1 ] ], "ro", linewidth = 1 );

plt.plot( [ worst_final[ 0 ] ], [ worst_final[ 1 ] ], "ro", linewidth = 1 );

# Initial orientation.

a1, b1 = rotate_point( arrow_size, 0.0, worst_initial[ 5 ] );
		
a1 = worst_initial[ 0 ] + a1;
b1 = worst_initial[ 1 ] + b1;

plt.annotate( 

	"", 
	xy = ( a1, b1 ), 
	xytext = ( worst_initial[ 0 ], worst_initial[ 1 ] ),
	arrowprops = dict( facecolor = "red", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )

);

# Final orientation.

a1, b1 = rotate_point( arrow_size, 0.0, worst_final[ 5 ] );
		
a1 = worst_final[ 0 ] + a1;
b1 = worst_final[ 1 ] + b1;

plt.annotate( 

	"", 
	xy = ( a1, b1 ), 
	xytext = ( worst_final[ 0 ], worst_final[ 1 ] ),
	arrowprops = dict( facecolor = "red", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )

);

'''

# Plot the best.

plt.plot( [ best_initial[ 0 ], best_final[ 0 ] ], [ best_initial[ 1 ], best_final[ 1 ] ], "--b", linewidth = 1 );

plt.plot( [ best_initial[ 0 ] ], [ best_initial[ 1 ] ], "bo", linewidth = 1 );

plt.plot( [ best_final[ 0 ] ], [ best_final[ 1 ] ], "bo", linewidth = 1 );

# Initial orientation.

a1, b1 = rotate_point( arrow_size, 0.0, best_initial[ 5 ] );
		
a1 = best_initial[ 0 ] + a1;
b1 = best_initial[ 1 ] + b1;

plt.annotate( 

	"", 
	xy = ( a1, b1 ), 
	xytext = ( best_initial[ 0 ], best_initial[ 1 ] ),
	arrowprops = dict( facecolor = "blue", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )

);

# Final orientation.

a1, b1 = rotate_point( arrow_size, 0.0, best_final[ 5 ] );
		
a1 = best_final[ 0 ] + a1;
b1 = best_final[ 1 ] + b1;

plt.annotate( 

	"", 
	xy = ( a1, b1 ), 
	xytext = ( best_final[ 0 ], best_final[ 1 ] ),
	arrowprops = dict( facecolor = "blue", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )

);

# Plot real robot centroid.

plt.plot( [ 0, real_robot_centroid[ 0 ] ], [ 0, real_robot_centroid[ 1 ] ], "--k", linewidth = 1 );

a1, b1 = rotate_point( arrow_size, 0.0, real_robot_centroid[ 2 ] );
		
a1 = 0.0 + a1;
b1 = 0.0 + b1;

plt.annotate( 

	"", 
	xy = ( a1, b1 ), 
	xytext = ( 0.0, 0.0 ),
	arrowprops = dict( facecolor = "black", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )

);

# X-t and Y-t.

plt.plot( [ real_robot_centroid[ 0 ] ], [ real_robot_centroid[ 1 ] ], "ko", linewidth = 1 );

# Z-r

a1, b1 = rotate_point( arrow_size, 0.0, real_robot_centroid[ 2 ] );
		
a1 = real_robot_centroid[ 0 ] + a1;
b1 = real_robot_centroid[ 1 ] + b1;

plt.annotate( 

	"", 
	xy = ( a1, b1 ), 
	xytext = ( real_robot_centroid[ 0 ], real_robot_centroid[ 1 ] ),
	arrowprops = dict( facecolor = "black", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )

);

plt.show( );

