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
plt.title( "BBAutoTune \n\n Experiment Three \n\n Highest Fitness" );
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

plt.show( );

