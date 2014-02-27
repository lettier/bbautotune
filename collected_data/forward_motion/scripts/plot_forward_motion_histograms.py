'''

David Lettier (C) 2014.

http://www.lettier.com/

Plots the normalized histograms for change in x, y, and theta.

'''

import matplotlib.pyplot as plt;
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

while line != "":
	
	splitted = line.split( ";" );
	
	x = float( splitted[ 0 ].rstrip( ) );
	y = float( splitted[ 1 ].rstrip( ) );
	t = float( splitted[ 2 ].rstrip( ) );
	
	x_p = float( splitted[ 4 ].rstrip( ) );
	y_p = float( splitted[ 5 ].rstrip( ) );
	t_p = float( splitted[ 6 ].rstrip( ) );
	
	x_trans = x - x;
	y_trans = x - x;
	
	x_p_trans = x_p - x;
	y_p_trans = y_p - y;
	
	x_p_rot, y_p_rot = rotate_point( x_p_trans, y_p_trans, -t );
	
	t_rot   = 0.0;
	t_p_rot = 0.0;
	
	if ( t < 0.0 ):
		
		t_rot = t - t;
		
	elif ( t >= 0.0 ):
		
		t_rot = t - t;
		
	if ( t < 0.0 and t_p < 0.0 ):
		
		t_p_rot = t_p - t;
		
	elif ( t >= 0.0 and t_p >= 0.0 ):
		
		t_p_rot = t_p - t;
		
	elif ( t >= 0.0 and t_p < 0.0 ):
		
		t_p_rot = t_p + t;
		
	elif ( t < 0.0 and t_p >= 0.0 ):
		
		t_p_rot = t_p + t;
		
	'''
		
	print "x", x, x_trans
	print "y", y, y_trans
	print "t", t, t_rot
	
	print "x_p", x_p, x_p_trans, x_p_rot
	print "y_p", y_p, y_p_trans, y_p_rot
	print "t_p", t_p, t_p_rot
	
	'''
	
	x_values.append( x_p_rot );
	
	y_values.append( y_p_rot );
	
	t_values.append( t_p_rot * ( 180.0 / math.pi ) );
	
	line = forward_file.readline( );
	
x_mean = sum( x_values ) * 1.0 / len( x_values );
x_var  = map( lambda a: ( a - x_mean ) ** 2, x_values );
x_var  = sum( x_var ) * 1.0 / len( x_var );
x_std  = math.sqrt( x_var );
	
print "X mean: ", x_mean;
print "X variance: ", x_var;
print "X standard deviation: ", x_std;

y_mean = sum( y_values ) * 1.0 / len( y_values );
y_var  = map( lambda a: ( a - y_mean ) ** 2, y_values );
y_var  = sum( y_var ) * 1.0 / len( y_var );
y_std  = math.sqrt( y_var );
	
print "Y mean: ", y_mean;
print "Y variance: ", y_var;
print "Y standard deviation: ", y_std;

t_mean = sum( t_values ) * 1.0 / len( t_values );
t_var  = map( lambda a: ( a - t_mean ) ** 2, t_values );
t_var  = sum( t_var ) * 1.0 / len( t_var );
t_std  = math.sqrt( t_var );
	
print "Theta mean: ", t_mean;
print "Theta variance: ", t_var;
print "Theta standard deviation: ", t_std; 
	
plt.subplot( 3, 1, 1 );
plt.hist( x_values, bins = 15, normed = True )
plt.title( "Real Robot Motion" )
plt.xlabel( "X-axis Delta in Centimeters" )
plt.ylabel( "Frequency Normalized" )
plt.grid( True )

plt.subplot( 3, 1, 2 );
plt.hist( y_values, bins = 15, normed = True )
plt.title( "Real Robot Motion" )
plt.xlabel( "Y-axis Delta in Centimeters" )
plt.ylabel( "Frequency Normalized" )
plt.grid( True )

plt.subplot( 3, 1, 3 );
plt.hist( t_values, bins = 15, normed = True )
plt.title( "Real Robot Motion" )
plt.xlabel( "Theta Delta in Degrees" )
plt.ylabel( "Frequency Normalized" )
plt.grid( True )

plt.tight_layout( pad = 1.08, h_pad = 0.5 );

plt.show( )