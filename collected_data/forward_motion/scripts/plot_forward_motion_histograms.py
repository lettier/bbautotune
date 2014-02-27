'''

David Lettier (C) 2014.

http://www.lettier.com/

Plots the normalized histograms for change in x, y, and theta.

'''
from mpl_toolkits.mplot3d import Axes3D;
import matplotlib.pyplot as plt;
from matplotlib import cm;
import numpy as np;
import math;

def rotate_point( x, y, angle_r ):
	
	x_rot = ( math.cos( angle_r ) * x ) + ( -math.sin( angle_r ) * y );
	y_rot = ( math.sin( angle_r ) * x ) + (  math.cos( angle_r ) * y );
	
	return x_rot, y_rot;

forward_file = open( "../processed_data/srv_1_forward.dat", "r" );

line = forward_file.readline( );

x_values = [ ];
y_values = [ ];
t_values = [ ];

x_p_values = [ ];
y_p_values = [ ];
t_p_values = [ ];

visualize_translation_rotation = False;

while line != "":
	
	splitted = line.split( ";" );
	
	x = float( splitted[ 0 ].rstrip( ) );
	y = float( splitted[ 1 ].rstrip( ) );
	t = float( splitted[ 2 ].rstrip( ) );
	
	x_p = float( splitted[ 4 ].rstrip( ) );
	y_p = float( splitted[ 5 ].rstrip( ) );
	t_p = float( splitted[ 6 ].rstrip( ) );
	
	x_tran = x - x;
	y_tran = x - x;
	
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
		
		print "t: ", t * ( 180.0 / math.pi );
		print "t_p: ", t_p * ( 180.0 / math.pi );
		print "t_rot: ", t_rot * ( 180.0 / math.pi );
		print "t_p_rot: ", t_p_rot * ( 180.0 / math.pi );
		
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
	
	x_values.append( x_tran_rot );
	
	y_values.append( y_tran_rot );
	
	t_values.append( t_rot * ( 180.0 / math.pi ) );	
	
	x_p_values.append( x_p_tran_rot );
	
	y_p_values.append( y_p_tran_rot );
	
	t_p_values.append( t_p_rot * ( 180.0 / math.pi ) );
	
	line = forward_file.readline( );
	
x_mean = sum( x_p_values ) * 1.0 / len( x_p_values );
x_var  = map( lambda a: ( a - x_mean ) ** 2, x_p_values );
x_var  = sum( x_var ) * 1.0 / len( x_var );
x_std  = math.sqrt( x_var );
	
print "X mean: ", x_mean;
print "X variance: ", x_var;
print "X standard deviation: ", x_std;

y_mean = sum( y_p_values ) * 1.0 / len( y_p_values );
y_var  = map( lambda a: ( a - y_mean ) ** 2, y_p_values );
y_var  = sum( y_var ) * 1.0 / len( y_var );
y_std  = math.sqrt( y_var );
	
print "Y mean: ", y_mean;
print "Y variance: ", y_var;
print "Y standard deviation: ", y_std;

t_mean = sum( t_p_values ) * 1.0 / len( t_p_values );
t_var  = map( lambda a: ( a - t_mean ) ** 2, t_p_values );
t_var  = sum( t_var ) * 1.0 / len( t_var );
t_std  = math.sqrt( t_var );
	
print "Theta mean: ", t_mean;
print "Theta variance: ", t_var;
print "Theta standard deviation: ", t_std; 

# First plot.

plt.figure( 1 );

plt.axis( "equal" );
	
plt.subplot( 3, 1, 1 );
plt.hist( x_p_values, bins = 15, normed = True );
plt.title( "Real Robot Forward Motion" );
plt.xlabel( "X-axis Delta in Centimeters" );
plt.ylabel( "Frequency Normalized" );
plt.grid( True );

plt.subplot( 3, 1, 2 );
plt.hist( y_p_values, bins = 15, normed = True );
plt.title( "Real Robot Forward Motion" );
plt.xlabel( "Y-axis Delta in Centimeters" );
plt.ylabel( "Frequency Normalized" );
plt.grid( True );

plt.subplot( 3, 1, 3 );
plt.hist( t_p_values, bins = 15, normed = True );
plt.title( "Real Robot Forward Motion" );
plt.xlabel( "Theta Delta in Degrees" );
plt.ylabel( "Frequency Normalized" );
plt.grid( True );

plt.tight_layout( pad = 1.08, h_pad = 0.5 );

# Second plot.

plt.figure( 2 );

plt.axis( "equal" );
plt.grid( True );
plt.title( "Real Robot Forward Motion" );
plt.xlabel( "X-axis" );
plt.ylabel( "Y-axis" );
plt.tight_layout( pad = 1.08, h_pad = 0.5 );

plt.plot( [ min( x_values ), max( x_p_values ) ], [ min( y_values ), min( y_values ) ], "r-", linewidth = 2 );

for i in range( len( x_p_values ) ):
	
	# Plot the starting point.
	
	plt.plot( [ x_values[ i ] ], [ y_values[ i ] ], "ro" );
	
	# Plot the start orientation.
	
	x_h, y_h = rotate_point( 2.0, 0.0, ( t_values[ i ] * ( math.pi / 180.0 ) ) );
	
	x_h = x_values[ i ] + x_h;
	y_h = y_values[ i ] + y_h;
	
	plt.annotate( 
		
		"", 
		xy = ( x_h, y_h ), 
		xytext = ( x_values[ i ], y_values[ i ] ),
		arrowprops = dict( facecolor = 'red', alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )
		
	);
	
	# Plot the traveled distance.
	
	xs = [ x_values[ i ], x_p_values[ i ] ];
	ys = [ y_values[ i ], y_p_values[ i ] ];
	
	plt.plot( xs, ys, "--g", linewidth = 1 );
	
	# Plot the resulting point.
	
	plt.plot( [ x_p_values[ i ] ], [ y_p_values[ i ] ], "bo", );
	
	# Plot the resulting orientation.
	
	x_p_h, y_p_h = rotate_point( 2.0, 0.0, ( t_p_values[ i ] * ( math.pi / 180.0 ) ) );
	
	x_p_h = x_p_values[ i ] + x_p_h;
	y_p_h = y_p_values[ i ] + y_p_h;
	
	plt.annotate( 
		
		"", 
		xy         = ( x_p_h, y_p_h ), 
		xytext     = ( x_p_values[ i ], y_p_values[ i ] ),
		arrowprops = dict( facecolor = 'blue', alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )
		
	);

# Third plot

fig = plt.figure( figsize = ( 12, 12 ) );
ax  = fig.gca( projection = "3d" );

ax.set_title(  "Real Robot Forward Motion",   fontsize = 15 );
ax.set_xlabel( "X-axis Delta in Centimeters", fontsize = 15 );
ax.set_ylabel( "Y-axis Delta in Centimeters", fontsize = 15 );
ax.set_zlabel( "\nTheta Delta in Degrees\n",    fontsize = 15, linespacing = 10 );

colors = [ ];
max_x  = max( x_p_values );
max_y  = max( y_p_values );
max_t  = max( t_p_values );

for i in range( len( x_p_values ) ):
	
	r = ( x_p_values[ i ] / max_x ) if ( x_p_values[ i ] >= 0.0 ) else 0.0;
	g = ( y_p_values[ i ] / max_y ) if ( y_p_values[ i ] >= 0.0 ) else 0.0;
	b = ( t_p_values[ i ] / max_t ) if ( t_p_values[ i ] >= 0.0 ) else 0.0;
	
	colors.append( [ r, g, b ] );

ax.scatter( x_p_values, y_p_values, t_p_values, alpha = 0.8, c = colors, s = 120, norm = True );

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

plt.show( )
