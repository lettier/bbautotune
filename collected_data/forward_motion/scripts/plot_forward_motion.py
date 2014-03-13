'''

David Lettier (C) 2014.

http://www.lettier.com/

Plots the real robot forward motion.

'''
import numpy as np;
import math;
import cPickle;
import matplotlib.pyplot as plt;
import matplotlib.mlab as mlab;
from mpl_toolkits.mplot3d import Axes3D;
from matplotlib import cm;
from matplotlib.patches import Rectangle;
from scipy.stats import scoreatpercentile;
from scipy.stats import normaltest;
from scipy.stats import norm;
from scipy.stats import probplot;

# Calculates or rather approximates the geometric median.

def calculate_geometric_median( candidate, a, b, c ):

	iterations = len( a );
	
	y = candidate;
	
	for i in range( iterations ):
		
		# Calculate the numerator.
		
		sum_n_a = 0.0;
		sum_n_b = 0.0;
		sum_n_c = 0.0;
		
		for j in range( len( a ) ):
			
			euclidean_distance = math.sqrt( ( a[ j ] - y[ 0 ] )**2.0 + ( b[ j ] - y[ 1 ] )**2.0 + ( c[ j ] - y[ 2 ] )**2.0 );
			
			sum_n_a += a[ j ] / euclidean_distance;
			sum_n_b += b[ j ] / euclidean_distance;
			sum_n_c += c[ j ] / euclidean_distance;
			
		# Calculate the denominator.
			
		sum_d_a = 0.0;
		sum_d_b = 0.0;
		sum_d_c = 0.0;
		
		for k in range( len( a ) ):
			
			euclidean_distance = math.sqrt( ( a[ k ] - y[ 0 ] )**2.0 + ( b[ k ] - y[ 1 ] )**2.0 + ( c[ k ] - y[ 2 ] )**2.0 );
			
			sum_d_a += 1.0 / euclidean_distance;
			sum_d_b += 1.0 / euclidean_distance;
			sum_d_c += 1.0 / euclidean_distance;
			
		y = [ sum_n_a / sum_d_a, sum_n_b / sum_d_b, sum_n_c / sum_d_c ];
		
	return y;

# Rotates a point around the origin, counter-clockwise.

def rotate_point( x, y, angle_r ):
	
	x_rot = ( math.cos( angle_r ) * x ) + ( -math.sin( angle_r ) * y );
	y_rot = ( math.sin( angle_r ) * x ) + (  math.cos( angle_r ) * y );
	
	return x_rot, y_rot;

forward_file = open( "../processed_data/srv_1_forward.dat", "r" );
#forward_file = open( "../raw_data/day3/run29.cfg", "r" );

line = forward_file.readline( );

x_originals = [ ];
y_originals = [ ];
t_originals = [ ];

x_p_originals = [ ];
y_p_originals = [ ];
t_p_originals = [ ];

x_values = [ ];
y_values = [ ];
t_values = [ ];

x_p_values = [ ];
y_p_values = [ ];
t_p_values = [ ];

visualize_translation_rotation = False;
line_i = 1;

while line != "":
	
	if ( line[ 0 ] == "#" ):
		
		# Ignore comments.
		
		line    = forward_file.readline( );
		line_i += 1;
		
		continue;
	
	splitted = line.split( ";" );
	
	x = float( splitted[ 0 ].rstrip( ) );
	y = float( splitted[ 1 ].rstrip( ) );
	t = float( splitted[ 2 ].rstrip( ) );
	
	x_p = float( splitted[ 4 ].rstrip( ) );
	y_p = float( splitted[ 5 ].rstrip( ) );
	t_p = float( splitted[ 6 ].rstrip( ) );
	
	x_tran = x - x;
	y_tran = y - y;
	
	x_tran_rot, y_tran_rot = rotate_point( x_tran, y_tran, -t );
	
	x_p_tran = x_p - x;
	y_p_tran = y_p - y;
	
	x_p_tran_rot, y_p_tran_rot = rotate_point( x_p_tran, y_p_tran, -t );
	
	t_rot   = 0.0;
	t_p_rot = 0.0;
	
	if ( t < 0.0 ):
		
		t_rot = t - t;
		
		t_p_rot = t_p - t;
		
	elif ( t >= 0.0 ):
		
		t_rot = t - t;
		
		t_p_rot = t_p - t;
	
	if ( visualize_translation_rotation ):
		
		# Zero plot.
		
		plt.figure( 0 );
		
		plt.plot( [ x, x_p ], [ y, y_p ], "--r", linewidth = 1 );
		
		plt.plot( [ x_p, x_p ], [ y_p, y_p ], "--ro", linewidth = 1 );
		
		plt.plot( [ x_tran, x_p_tran ], [ y_tran, y_p_tran ], "--b", linewidth = 1 );
		
		plt.plot( [ x_p_tran, x_p_tran ], [ y_p_tran, y_p_tran ], "--bo", linewidth = 1 );
		
		plt.plot( [ x_tran_rot, x_p_tran_rot ], [ y_tran_rot, y_p_tran_rot ], "--g", linewidth = 1 );
		
		plt.plot( [ x_p_tran_rot, x_p_tran_rot ], [ y_p_tran_rot, y_p_tran_rot ], "--go", linewidth = 1 );
		
		print "---";
		
		print "Line number: ", line_i;
		
		print "x: ", x;
		print "x_tran: ", x_tran;
		print "x_tran_rot: ", x_tran_rot;
		print "x_p: ", x_p;
		print "x_p_tran: ", x_p_tran;
		print "x_p_tran_rot: ", x_p_tran_rot;
		
		print "y: ", y;
		print "y_tran: ", y_tran;
		print "y_tran_rot: ", y_tran_rot;
		print "y_p: ", y_p;
		print "y_p_tran: ", y_p_tran;
		print "y_p_tran_rot: ", y_p_tran_rot;
		
		print "t: ",       t,       ( t * ( 180.0 / math.pi ) )       % 360.0;
		print "t_p: ",     t_p,     ( t_p * ( 180.0 / math.pi ) )     % 360.0;
		print "t_rot: ",   t_rot,   ( t_rot * ( 180.0 / math.pi ) )   % 360.0;
		print "t_p_rot: ", t_p_rot, ( t_p_rot * ( 180.0 / math.pi ) ) % 360.0;
		
		# Not translated nor rotated.
		
		a1, b1 = rotate_point( 10, 0, t );
		
		a1 = x + a1;
		b1 = y + b1;

		plt.annotate( 
		
			"", 
			xy = ( a1, b1 ), 
			xytext = ( x, y ),
			arrowprops = dict( facecolor = "red", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )
		
		);
		
		a2, b2 = rotate_point( 10, 0, t_p );
		
		a2 = x_p + a2;
		b2 = y_p + b2;

		plt.annotate( 
		
			"", 
			xy = ( a2, b2 ), 
			xytext = ( x_p, y_p ),
			arrowprops = dict( facecolor = "red", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )
		
		);
		
		# Translated.
		
		a3, b3 = rotate_point( 10, 0, t );
		
		a3 = x_tran + a3;
		b3 = y_tran + b3;

		plt.annotate( 
		
			"", 
			xy = ( a3, b3 ), 
			xytext = ( x_tran, y_tran ),
			arrowprops = dict( facecolor = "blue", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )
		
		);
		
		a4, b4 = rotate_point( 10, 0, t_p );
		
		a4 = x_p_tran + a4;
		b4 = y_p_tran + b4;

		plt.annotate( 
		
			"", 
			xy = ( a4, b4 ), 
			xytext = ( x_p_tran, y_p_tran ),
			arrowprops = dict( facecolor = "blue", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )
		
		);
		
		# Translated rotated.
		
		a5, b5 = rotate_point( 10, 0, t_rot );
		
		a5 = x_tran_rot + a5;
		b5 = y_tran_rot + b5;

		plt.annotate( 
		
			"", 
			xy = ( a5, b5 ), 
			xytext = ( x_tran_rot, y_tran_rot ),
			arrowprops = dict( facecolor = "green", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )
		
		);
		
		a6, b6 = rotate_point( 10, 0, t_p_rot );
		
		a6 = x_p_tran_rot + a6;
		b6 = y_p_tran_rot + b6;

		plt.annotate( 
		
			"", 
			xy = ( a6, b6 ), 
			xytext = ( x_p_tran_rot, y_p_tran_rot ),
			arrowprops = dict( facecolor = "green", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )
		
		);
		
		plt.axis( "equal" );
		
		plt.grid( True );
		
		plt.show( );
		
	x_originals.append( x );
	y_originals.append( y );
	t_originals.append( t );
	
	x_p_originals.append( x_p );
	y_p_originals.append( y_p );
	t_p_originals.append( t_p );
	
	x_values.append( x_tran_rot );
	y_values.append( y_tran_rot );
	#t_values.append( ( t_rot * ( 180.0 / math.pi ) ) % 360.0 );
	t_values.append( t_rot );
	
	x_p_values.append( x_p_tran_rot );
	y_p_values.append( y_p_tran_rot );
	#t_p_values.append( ( t_p_rot * ( 180.0 / math.pi ) ) % 360.0 );
	t_p_values.append( t_p_rot );
	
	line    = forward_file.readline( );
	line_i += 1;
	
cPickle.dump( x_originals, open( "../pickled_data/x_originals.pkl", "wb" ) );
cPickle.dump( y_originals, open( "../pickled_data/y_originals.pkl", "wb" ) );
cPickle.dump( t_originals, open( "../pickled_data/t_originals.pkl", "wb" ) );

cPickle.dump( x_p_originals, open( "../pickled_data/x_p_originals.pkl", "wb" ) );
cPickle.dump( y_p_originals, open( "../pickled_data/y_p_originals.pkl", "wb" ) );
cPickle.dump( t_p_originals, open( "../pickled_data/t_p_originals.pkl", "wb" ) );
	
cPickle.dump( x_values, open( "../pickled_data/x_values.pkl", "wb" ) );
cPickle.dump( y_values, open( "../pickled_data/y_values.pkl", "wb" ) );
cPickle.dump( t_values, open( "../pickled_data/t_values.pkl", "wb" ) );

cPickle.dump( x_p_values, open( "../pickled_data/x_p_values.pkl", "wb" ) );
cPickle.dump( y_p_values, open( "../pickled_data/y_p_values.pkl", "wb" ) );
cPickle.dump( t_p_values, open( "../pickled_data/t_p_values.pkl", "wb" ) );

print "Number of sample points: ", line_i;
	
# X'Y'T' stats.
	
x_p_mean = sum( x_p_values ) / float( len( x_p_values ) );
x_p_var  = map( lambda a: ( a - x_p_mean )**2.0, x_p_values );
x_p_var  = sum( x_p_var ) / float( len( x_p_var ) );
x_p_std  = math.sqrt( x_p_var );

print "X' max/min: ", max( x_p_values ), min( x_p_values );
print "X' mean: ", x_p_mean;
print "X' variance: ", x_p_var;
print "X' standard deviation: ", x_p_std;

y_p_mean = sum( y_p_values ) / float( len( y_p_values ) );
y_p_var  = map( lambda a: ( a - y_p_mean )**2.0, y_p_values );
y_p_var  = sum( y_p_var ) / float( len( y_p_var ) );
y_p_std  = math.sqrt( y_p_var );

print "Y' max/min: ", max( y_p_values ), min( y_p_values );
print "Y' mean: ", y_p_mean;
print "Y' variance: ", y_p_var;
print "Y' standard deviation: ", y_p_std;

t_p_mean = sum( t_p_values ) / float( len( t_p_values ) );
t_p_var  = map( lambda a: ( a - t_p_mean )**2.0, t_p_values );
t_p_var  = sum( t_p_var ) / float( len( t_p_var ) );
t_p_std  = math.sqrt( t_p_var );

print "Theta' max/min: ", max( t_p_values ), min( t_p_values );
print "Theta' mean: ", t_p_mean;
print "Theta' variance: ", t_p_var;
print "Theta' standard deviation: ", t_p_std;

z, x_p_normal_test = normaltest( x_p_values, axis = 0 );
z, y_p_normal_test = normaltest( y_p_values, axis = 0 );
z, t_p_normal_test = normaltest( t_p_values, axis = 0 );

x_p_is_normal = "Normal";
y_p_is_normal = "Normal";
t_p_is_normal = "Normal";

if ( x_p_normal_test < 0.05 ):
	
	x_p_is_normal = "Not Normal";
	
if ( y_p_normal_test < 0.05 ):
	
	y_p_is_normal = "Not Normal";
	
if ( t_p_normal_test < 0.05 ):
	
	t_p_is_normal = "Not Normal";

print "X' normal test p-value: ", x_p_normal_test, x_p_is_normal;
print "Y' normal test p-value: ", y_p_normal_test, y_p_is_normal;
print "T' normal test p-value: ", t_p_normal_test, t_p_is_normal;

# Covariance matrix.

forward_motion = [ ];

for i in range( len( x_p_values ) ):
	
	x_p_value = x_p_values[ i ];
	y_p_value = y_p_values[ i ];
	t_p_value = t_p_values[ i ];
	
	forward_motion.append( 
		
		[ x_p_value, y_p_value, t_p_value ]
		
	);
	
print "Covariance matrix: ";
print np.cov( forward_motion, rowvar = 0 );

# Find the median of each dimension.

x_p_median = 0.0;
y_p_median = 0.0;
t_p_median = 0.0;

x_p_sorted = sorted( x_p_values );
y_p_sorted = sorted( y_p_values );
t_p_sorted = sorted( t_p_values );

if ( len( x_p_sorted ) % 2 == 0 ): # Even.
	
	x_p_median = ( x_p_sorted[ ( len( x_p_sorted ) / 2 ) - 1 ] + x_p_sorted[ ( len( x_p_sorted ) / 2 ) ] ) / 2.0;
	y_p_median = ( y_p_sorted[ ( len( y_p_sorted ) / 2 ) - 1 ] + y_p_sorted[ ( len( y_p_sorted ) / 2 ) ] ) / 2.0; 
	t_p_median = ( t_p_sorted[ ( len( t_p_sorted ) / 2 ) - 1 ] + t_p_sorted[ ( len( t_p_sorted ) / 2 ) ] ) / 2.0;
	
else:
	
	x_p_median = x_p_sorted[ ( len( x_p_sorted ) / 2 ) ];
	y_p_median = y_p_sorted[ ( len( y_p_sorted ) / 2 ) ]; 
	t_p_median = t_p_sorted[ ( len( t_p_sorted ) / 2 ) ];
	
print "X', Y', T' Median: ", x_p_median, ", ", y_p_median, ", ", t_p_median;
	
# Find the centroid. 

xyt_p_centroid = [ ];

xyt_p_centroid.append( sum( x_p_values ) / float( len( x_p_values ) ) );
xyt_p_centroid.append( sum( y_p_values ) / float( len( y_p_values ) ) );
xyt_p_centroid.append( sum( t_p_values ) / float( len( t_p_values ) ) );

print "X'Y'T' Centroid: ", xyt_p_centroid[ 0 ], ", ", xyt_p_centroid[ 1 ], ", ", xyt_p_centroid[ 2 ];

# Find the geometric median.

xyt_p_geometric_median = calculate_geometric_median(
	
	[ x_p_median, y_p_median, t_p_median ],
	x_p_values,
	y_p_values,
	t_p_values
	
);

print "X'Y'T' Geometric Median: ", xyt_p_geometric_median[ 0 ], ", ", xyt_p_geometric_median[ 1 ], ", ", xyt_p_geometric_median[ 2 ];

# First plot.

plt.figure( 1 );

plt.title( "Total Original Real Robot Motion Collected (Camera Perspective)" );
	
plt.axis( "equal" );

plt.xlabel( "X-axis in Centimeters" );
plt.ylabel( "Y-axis in Centimeters" );

plt.grid( True );

color_percentage = 0.0;

x_previous = 0.0;
y_previous = 0.0;

start = 0;
stop  = len( x_originals );

for i in range( start, stop ):
	
	color_percentage = float( i ) / float( len( x_originals ) );
	
	if ( x_originals[ i ] == x_previous and y_originals[ i ] == y_previous ):
	
		plt.plot( 
			
			[ x_originals[ i ] ], 
			[ y_originals[ i ] ],
			"o",
			color = "green"
			
		);
		
	else:
		
		plt.plot( 
			
			[ x_originals[ i ] ], 
			[ y_originals[ i ] ],
			"*",
			markersize = 10,
			color = "green"
			
		);
	
	plt.plot( 
		
		[ x_originals[ i ], x_p_originals[ i ] ], 
		[ y_originals[ i ], y_p_originals[ i ] ],
		"--",
		color = str( color_percentage )
		
	);
	
	if ( i + 1 == stop ):
		
		plt.plot( 
			
			[ x_p_originals[ i ] ], 
			[ y_p_originals[ i ] ],
			"*",
			markersize = 10,
			color = "red"
			
		);
	
	elif ( x_p_originals[ i ] == x_originals[ i + 1 ] and y_p_originals[ i ] == y_originals[ i + 1 ] ):
	
		plt.plot( 
			
			[ x_p_originals[ i ] ], 
			[ y_p_originals[ i ] ],
			"o",
			color = "red"
			
		);
		
	else:
		
		plt.plot( 
			
			[ x_p_originals[ i ] ], 
			[ y_p_originals[ i ] ],
			"*",
			markersize = 10,
			color = "red"
			
		);
	
	a1, b1 = rotate_point( 10, 0, t_originals[ i ] );
		
	a1 = x_originals[ i ] + a1;
	b1 = y_originals[ i ] + b1;

	plt.annotate( 
	
		"", 
		xy = ( a1, b1 ), 
		xytext = ( x_originals[ i ], y_originals[ i ] ),
		arrowprops = dict( facecolor = str( color_percentage ), alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )
	
	);
	
	a2, b2 = rotate_point( 10, 0, t_p_originals[ i ] );
		
	a2 = x_p_originals[ i ] + a2;
	b2 = y_p_originals[ i ] + b2;

	plt.annotate( 
	
		"", 
		xy = ( a2, b2 ), 
		xytext = ( x_p_originals[ i ], y_p_originals[ i ] ),
		arrowprops = dict( facecolor = str( color_percentage ), alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )
	
	);
	
	x_previous = x_p_originals[ i ];
	y_previous = y_p_originals[ i ];

# Second plot.

# Calculate the Freedman-Diaconis' choice for bin size.

X_sorted = np.sort( x_p_values );

Q3 = scoreatpercentile( X_sorted, 75 );
Q1 = scoreatpercentile( X_sorted, 25 );

IQR = Q3 - Q1;

h = 2.0 * ( IQR / ( len( X_sorted )**( 1.0 / 3.0 ) ) );

k_x = math.ceil( ( max( x_p_values ) - min( x_p_values ) ) / h );

plt.figure( 2 );

plt.subplot( 3, 1, 1 );
n, bins, patches = plt.hist( x_p_values, bins = k_x, normed = True, alpha = 0.75, histtype = "stepfilled" );
max_patch_height = max( ( np.histogram( x_p_values, k_x, normed = True ) )[ 0 ] );
normal_pdf       = mlab.normpdf( bins, x_p_mean, x_p_std );
plt.plot( bins, normal_pdf, "r--", linewidth = 1 );
current_axis = plt.gca( );
current_axis.add_patch( Rectangle( ( ( x_p_mean - x_p_std ), 0.0 ), x_p_std, max_patch_height, facecolor = "grey", alpha = 0.5 ) );
current_axis.add_patch( Rectangle( ( ( x_p_mean ), 0.0 ), x_p_std, max_patch_height, facecolor = "grey", alpha = 0.5 ) );
plt.plot( [ x_p_mean, x_p_mean ], [ 0.0, max_patch_height ], "g--", linewidth = 3 );
plt.plot( [ ( x_p_mean - x_p_std ), ( x_p_mean - x_p_std ) ], [ 0.0, max_patch_height ], "c--", linewidth = 3 );
plt.plot( [ ( x_p_mean + x_p_std ), ( x_p_mean + x_p_std ) ], [ 0.0, max_patch_height ], "c--", linewidth = 3 );
plt.plot( [ x_p_median, x_p_median ], [ 0.0, max_patch_height ], "k--", linewidth = 3 );
plt.title( "Real Robot Forward Motion" );
plt.xlabel( "X-axis Delta in Centimeters" );
plt.ylabel( "PDF Normalized" );
plt.grid( True );

Y_sorted = np.sort( y_p_values );

Q3 = scoreatpercentile( Y_sorted, 75 );
Q1 = scoreatpercentile( Y_sorted, 25 );

IQR = Q3 - Q1;

h = 2.0 * ( IQR / ( len( Y_sorted )**( 1.0 / 3.0 ) ) );

k_y = math.ceil( ( max( y_p_values ) - min( y_p_values ) ) / h );

plt.subplot( 3, 1, 2 );
n, bins, patches = plt.hist( y_p_values, bins = k_y, normed = True, alpha = 0.75, histtype = "stepfilled" );
max_patch_height = max( ( np.histogram( y_p_values, k_y, normed = True ) )[ 0 ] );
normal_pdf       = mlab.normpdf( bins, y_p_mean, y_p_std );
plt.plot( bins, normal_pdf, "r--", linewidth = 1 );
current_axis = plt.gca( );
current_axis.add_patch( Rectangle( ( ( y_p_mean - y_p_std ), 0.0 ), y_p_std, max_patch_height, facecolor = "grey", alpha = 0.5 ) );
current_axis.add_patch( Rectangle( ( ( y_p_mean ), 0.0 ), y_p_std, max_patch_height, facecolor = "grey", alpha = 0.5 ) );
plt.plot( [ y_p_mean, y_p_mean ], [ 0.0, max_patch_height ], "g--", linewidth = 3 );
plt.plot( [ ( y_p_mean - y_p_std ), ( y_p_mean - y_p_std ) ], [ 0.0, max_patch_height ], "c--", linewidth = 3 );
plt.plot( [ ( y_p_mean + y_p_std ), ( y_p_mean + y_p_std ) ], [ 0.0, max_patch_height ], "c--", linewidth = 3 );
plt.plot( [ y_p_median, y_p_median ], [ 0.0, max_patch_height ], "k--", linewidth = 3 );
plt.title( "Real Robot Forward Motion" );
plt.xlabel( "Y-axis Delta in Centimeters" );
plt.ylabel( "PDF Normalized" );
plt.grid( True );

T_sorted = np.sort( t_p_values );

Q3 = scoreatpercentile( T_sorted, 75 );
Q1 = scoreatpercentile( T_sorted, 25 );

IQR = Q3 - Q1;

h = 2.0 * ( IQR / ( len( T_sorted )**( 1.0 / 3.0 ) ) );

k_t = math.ceil( ( max( t_p_values ) - min( t_p_values ) ) / h );

plt.subplot( 3, 1, 3 );
n, bins, patches = plt.hist( t_p_values, bins = k_t, normed = True, alpha = 0.75, histtype = "stepfilled" );
max_patch_height = max( ( np.histogram( t_p_values, k_t, normed = True ) )[ 0 ] );
normal_pdf       = mlab.normpdf( bins, t_p_mean, t_p_std );
plt.plot( bins, normal_pdf, "r--", linewidth = 1 );
current_axis = plt.gca( );
current_axis.add_patch( Rectangle( ( ( t_p_mean - t_p_std ), 0.0 ), t_p_std, max_patch_height, facecolor = "grey", alpha = 0.5 ) );
current_axis.add_patch( Rectangle( ( ( t_p_mean ), 0.0 ), t_p_std, max_patch_height, facecolor = "grey", alpha = 0.5 ) );
plt.plot( [ t_p_mean, t_p_mean ], [ 0.0, max_patch_height ], "g--", linewidth = 3 );
plt.plot( [ ( t_p_mean - t_p_std ), ( t_p_mean - t_p_std ) ], [ 0.0, max_patch_height ], "c--", linewidth = 3 );
plt.plot( [ ( t_p_mean + t_p_std ), ( t_p_mean + t_p_std ) ], [ 0.0, max_patch_height ], "c--", linewidth = 3 );
plt.plot( [ t_p_median, t_p_median ], [ 0.0, max_patch_height ], "k--", linewidth = 3 );
plt.title( "Real Robot Forward Motion" );
plt.xlabel( "Theta Delta in Degrees" );
plt.ylabel( "PDF Normalized" );
plt.grid( True );

plt.tight_layout( pad = 1.08, h_pad = 0.5 );

# Third plot.

plt.figure( 3 );

plt.subplot( 3, 1, 1 );
plt.hist( x_p_values, bins = k_x, normed = True, alpha = 0.75, cumulative = True, histtype = "stepfilled" );
normal_data = sorted( norm.rvs( size = len( x_p_values ), loc = x_p_mean, scale = x_p_std ) );
normal_data_cdf = norm.cdf( normal_data, x_p_mean, x_p_std );
plt.plot( normal_data, normal_data_cdf, "--r" );
plt.title( "Real Robot Forward Motion" );
plt.xlabel( "X-axis Delta in Centimeters" );
plt.ylabel( "CDF Normalized" );
plt.grid( True );

plt.subplot( 3, 1, 2 );
plt.hist( y_p_values, bins = k_y, normed = True, alpha = 0.75, cumulative = True, histtype = "stepfilled" );
normal_data = sorted( norm.rvs( size = len( y_p_values ), loc = y_p_mean, scale = y_p_std ) );
normal_data_cdf = norm.cdf( normal_data, y_p_mean, y_p_std );
plt.plot( normal_data, normal_data_cdf, "--r" );
plt.title( "Real Robot Forward Motion" );
plt.xlabel( "Y-axis Delta in Centimeters" );
plt.ylabel( "CDF Normalized" );
plt.grid( True );

plt.subplot( 3, 1, 3 );
plt.hist( t_p_values, bins = k_t, normed = True, alpha = 0.75, cumulative = True, histtype = "stepfilled" );
normal_data = sorted( norm.rvs( size = len( t_p_values ), loc = t_p_mean, scale = t_p_std ) );
normal_data_cdf = norm.cdf( normal_data, t_p_mean, t_p_std );
plt.plot( normal_data, normal_data_cdf, "--r" );
plt.title( "Real Robot Forward Motion" );
plt.xlabel( "Theta Delta in Degrees" );
plt.ylabel( "CDF Normalized" );
plt.grid( True );

plt.tight_layout( pad = 1.08, h_pad = 0.5 );

# Fourth plot.

plt.figure( 4 );

plt.axis( "equal" );
plt.grid( True );
plt.title( "Real Robot Forward Motion (Robot Perspective)" );
plt.xlabel( "X-axis" );
plt.ylabel( "Y-axis" );
plt.tight_layout( pad = 1.08, h_pad = 0.5 );

plt.plot( [ min( x_values ), max( x_p_values ) ], [ min( y_values ), min( y_values ) ], "r-", linewidth = 2 );

for i in range( len( x_p_values ) ):
	
	# Plot the starting point.
	
	plt.plot( [ x_values[ i ] ], [ y_values[ i ] ], "go" );
	
	# Plot the start orientation.
	
	#x_h, y_h = rotate_point( 2.0, 0.0, ( t_values[ i ] * ( math.pi / 180.0 ) ) );
	x_h, y_h = rotate_point( 2.0, 0.0, t_values[ i ] );
	
	x_h = x_values[ i ] + x_h;
	y_h = y_values[ i ] + y_h;
	
	plt.annotate( 
		
		"", 
		xy = ( x_h, y_h ), 
		xytext = ( x_values[ i ], y_values[ i ] ),
		arrowprops = dict( facecolor = 'green', alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )
		
	);
	
	# Plot the traveled distance.
	
	xs = [ x_values[ i ], x_p_values[ i ] ];
	ys = [ y_values[ i ], y_p_values[ i ] ];
	
	plt.plot( xs, ys, "--b", linewidth = 1 );
	
	# Plot the resulting point.
	
	plt.plot( [ x_p_values[ i ] ], [ y_p_values[ i ] ], "ro", );
	
	# Plot the resulting orientation.
	
	#x_p_h, y_p_h = rotate_point( 2.0, 0.0, ( t_p_values[ i ] * ( math.pi / 180.0 ) ) );
	x_p_h, y_p_h = rotate_point( 2.0, 0.0, t_p_values[ i ] );
	
	x_p_h = x_p_values[ i ] + x_p_h;
	y_p_h = y_p_values[ i ] + y_p_h;
	
	plt.annotate( 
		
		"", 
		xy         = ( x_p_h, y_p_h ), 
		xytext     = ( x_p_values[ i ], y_p_values[ i ] ),
		arrowprops = dict( facecolor = 'red', alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )
		
	);
	
# Plot 5.
	
plt.figure( 5 );

plt.subplot( 3, 1, 1 );
plt.grid( True );
x_qq_plot = probplot( x_p_values, dist = "norm", sparams = ( x_p_mean, x_p_std ), plot = plt );
plt.title( "Real Robot Forward Motion Q-Q Plot" );
plt.xlabel( "Normal Quantile" );
plt.ylabel( "Ordered X-axis Delta Quantile" );

plt.subplot( 3, 1, 2 );
plt.grid( True );
x_qq_plot = probplot( y_p_values, dist = "norm", sparams = ( y_p_mean, y_p_std ), plot = plt );
plt.title( "Real Robot Forward Motion Q-Q Plot" );
plt.xlabel( "Normal Quantile" );
plt.ylabel( "Ordered Y-axis Delta Quantile" );

plt.subplot( 3, 1, 3 );
plt.grid( True );
x_qq_plot = probplot( t_p_values, dist = "norm", sparams = ( t_p_mean, t_p_std ), plot = plt );
plt.title( "Real Robot Forward Motion Q-Q Plot" );
plt.xlabel( "Normal Quantile" );
plt.ylabel( "Ordered Theta Delta Quantile" );

# Plot 6.

# Begin plotting the 3D scatter plot.

fig = plt.figure( 6, figsize = ( 12, 12 ) );
ax  = fig.gca( projection = "3d" );

ax.grid( alpha = 1.0 );

ax.set_title(  "Real Robot Forward Motion",   fontsize = 15 );
ax.set_xlabel( "X-axis Delta in Centimeters", fontsize = 15 );
ax.set_ylabel( "Y-axis Delta in Centimeters", fontsize = 15 );
ax.set_zlabel( "Theta Delta in Radians",  fontsize = 15, linespacing = 10 );

colors = [ ];
max_x  = max( x_p_values );
max_y  = max( y_p_values );
max_t  = max( t_p_values );

for i in range( len( x_p_values ) ):
	
	r = ( x_p_values[ i ] / max_x ) if ( x_p_values[ i ] >= 0.0 ) else 0.0;
	g = ( y_p_values[ i ] / max_y ) if ( y_p_values[ i ] >= 0.0 ) else 0.0;
	b = ( t_p_values[ i ] / max_t ) if ( t_p_values[ i ] >= 0.0 ) else 0.0;
	
	colors.append( [ r, g, b ] );

# Plot the points.

ax.scatter( x_p_values, y_p_values, t_p_values, alpha = 0.5, c = colors, s = 120, norm = True );

# Plot the centroid.

ax.plot( [ xyt_p_centroid[ 0 ] ], [ xyt_p_centroid[ 1 ] ], [ xyt_p_centroid[ 2 ] ], color = "w", marker = "*", ms = 20 );

# Plot the median.

ax.plot( [ x_p_median ], [ y_p_median ], [ t_p_median ], color = "w", marker = "d", ms = 20 );

# Plot the geometric median.

ax.plot( [ xyt_p_geometric_median[ 0 ] ], [ xyt_p_geometric_median[ 1 ] ], [ xyt_p_geometric_median[ 2 ] ], color = "w", marker = "h", ms = 20 );

ax.set_xlim3d( min( x_p_values ), max( x_p_values ) );
ax.set_ylim3d( min( y_p_values ), max( y_p_values ) ); 
ax.set_zlim3d( min( t_p_values ), max( t_p_values ) ); 

for xtick in ax.xaxis.get_major_ticks( ):
	
	xtick.label.set_fontsize( 15 );
	
for ytick in ax.yaxis.get_major_ticks( ):

	ytick.label.set_fontsize( 15 );
	
for ztick in ax.zaxis.get_major_ticks( ):

	ztick.label.set_fontsize( 15 );

plt.subplots_adjust( left = 0.0, right = 1.0, top = 1.0, bottom = 0.0 );

plt.show( );
