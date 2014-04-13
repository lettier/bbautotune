'''

David Lettier (C) 2014.

http://www.lettier.com/

Plots a BBAutoTune GA experiment.

'''

import sys;
import numpy;
import math;
import pickle;
import matplotlib.pyplot as plt;
import matplotlib.mlab as mlab;
from mpl_toolkits.mplot3d import Axes3D;
from matplotlib import cm;
from matplotlib.patches import Rectangle;
import scipy.spatial.distance;
from sklearn.covariance import MinCovDet;

# Import real robot forward motion data.

x_p_values = pickle.load( open( "../../collected_data/forward_motion/pickled_data/x_p_values.pkl", "rb" ) );
y_p_values = pickle.load( open( "../../collected_data/forward_motion/pickled_data/y_p_values.pkl", "rb" ) );
t_p_values = pickle.load( open( "../../collected_data/forward_motion/pickled_data/t_p_values.pkl", "rb" ) );

forward_motion = [ ];

for i in range( len( x_p_values ) ):
	
	x_p_value = x_p_values[ i ];
	y_p_value = y_p_values[ i ];
	t_p_value = t_p_values[ i ];
	
	forward_motion.append( 
		
		[ x_p_value, y_p_value, t_p_value ]
		
	);
	
# Get the robust distances.
	
forward_motion = numpy.array( forward_motion );

mcd_trained = MinCovDet( assume_centered = False, support_fraction = 0.5 * ( len( forward_motion ) + 3.0 + 1.0 ) ).fit( forward_motion );

rml     = mcd_trained.location_;
rcm_inv = numpy.linalg.inv( mcd_trained.covariance_ );

rrrd = scipy.spatial.distance.mahalanobis( rml, rml, rcm_inv );

exp2_best_initial = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ];
exp2_best_final   = [ 23.123499751091003, .009536895231576636, 0.0, 0.0, -0.0, 0.002033736789599061 ];

exp2rd = scipy.spatial.distance.mahalanobis( [ exp2_best_final[ 0 ], exp2_best_final[ 1 ], exp2_best_final[ 5 ] ], rml, rcm_inv );

exp3_best_initial = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ];
exp3_best_final   = [ 23.95108938217163, -0.3489761846140027, 0.0, 0.0, 0.0, -0.00318596581928432 ];

exp3rd = scipy.spatial.distance.mahalanobis( [ exp3_best_final[ 0 ], exp3_best_final[ 1 ], exp3_best_final[ 5 ] ], rml, rcm_inv );

exp4_best_initial = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ];
exp4_best_final   = [ 23.491448163986206, -0.002863347253878601, 0.0, 0.0 ,0.0, -0.004287547431886196 ];

exp4rd = scipy.spatial.distance.mahalanobis( [ exp4_best_final[ 0 ], exp4_best_final[ 1 ], exp4_best_final[ 5 ] ], rml, rcm_inv );

exp5_best_initial = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ];
exp5_best_final   = [ 24.055466055870056, 0.016411948308814317, 0.0, 0.0, -0.0, 0.0011841553496196866 ];

exp5rd = scipy.spatial.distance.mahalanobis( [ exp5_best_final[ 0 ], exp5_best_final[ 1 ], exp5_best_final[ 5 ] ], rml, rcm_inv );

# Rotates a point around the origin, counter-clockwise.

def rotate_point( x, y, angle_r ):
	
	x_rot = ( math.cos( angle_r ) * x ) + ( -math.sin( angle_r ) * y );
	y_rot = ( math.sin( angle_r ) * x ) + (  math.cos( angle_r ) * y );
	
	return x_rot, y_rot;

real_robot_centroid_classic = [ 23.8644631679, 0.338269853117, -0.00417473025048 ]; # Classical mean.

real_robot_centroid_robust = rml; # Robust mean.

plt.figure( 1 );

plt.title( "BBAutoTune \n\n Simulated Motion versus Real Motion" );
plt.ylabel( "Y-position in Centimeters" );
plt.xlabel( "X-position in Centimeters" );
plt.grid( True );
plt.axis( "equal" );

arrow_size = 0.1;

#--------------------------------------------------------------------------

# Experiment two.

# Plot initial x-t, y-t to final x-t, y-t.

plt.plot( [ exp2_best_initial[ 0 ], exp2_best_final[ 0 ] ], [ exp2_best_initial[ 1 ], exp2_best_final[ 1 ] ], "--b", linewidth = 1 );

# Plot initial x-t, y-t.

plt.plot( [ exp2_best_initial[ 0 ] ], [ exp2_best_initial[ 1 ] ], "bo", linewidth = 1 );

# Plot final x-y, y-t.

plt.plot( [ exp2_best_final[ 0 ] ], [ exp2_best_final[ 1 ] ], "bo", linewidth = 1 );

# Initial orientation.

a1, b1 = rotate_point( arrow_size, 0.0, exp2_best_initial[ 5 ] );
		
a1 = exp2_best_initial[ 0 ] + a1;
b1 = exp2_best_initial[ 1 ] + b1;

plt.annotate( 

	"", 
	xy = ( a1, b1 ), 
	xytext = ( exp2_best_initial[ 0 ], exp2_best_initial[ 1 ] ),
	arrowprops = dict( facecolor = "blue", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )

);

# Final orientation.

a1, b1 = rotate_point( arrow_size, 0.0, exp2_best_final[ 5 ] );
		
a1 = exp2_best_final[ 0 ] + a1;
b1 = exp2_best_final[ 1 ] + b1;

plt.annotate( 

	"", 
	xy = ( a1, b1 ), 
	xytext = ( exp2_best_final[ 0 ], exp2_best_final[ 1 ] ),
	arrowprops = dict( facecolor = "blue", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )

);

#--------------------------------------------------------------------------

# Experiment three.

# Plot initial x-t, y-t to final x-t, y-t.

plt.plot( [ exp3_best_initial[ 0 ], exp3_best_final[ 0 ] ], [ exp3_best_initial[ 1 ], exp3_best_final[ 1 ] ], "--r", linewidth = 1 );

# Plot initial x-t, y-t.

plt.plot( [ exp3_best_initial[ 0 ] ], [ exp3_best_initial[ 1 ] ], "ro", linewidth = 1 );

# Plot final x-y, y-t.

plt.plot( [ exp3_best_final[ 0 ] ], [ exp3_best_final[ 1 ] ], "ro", linewidth = 1 );

# Initial orientation.

a1, b1 = rotate_point( arrow_size, 0.0, exp3_best_initial[ 5 ] );
		
a1 = exp3_best_initial[ 0 ] + a1;
b1 = exp3_best_initial[ 1 ] + b1;

plt.annotate( 

	"", 
	xy = ( a1, b1 ), 
	xytext = ( exp3_best_initial[ 0 ], exp3_best_initial[ 1 ] ),
	arrowprops = dict( facecolor = "red", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )

);

# Final orientation.

a1, b1 = rotate_point( arrow_size, 0.0, exp3_best_final[ 5 ] );
		
a1 = exp3_best_final[ 0 ] + a1;
b1 = exp3_best_final[ 1 ] + b1;

plt.annotate( 

	"", 
	xy = ( a1, b1 ), 
	xytext = ( exp3_best_final[ 0 ], exp3_best_final[ 1 ] ),
	arrowprops = dict( facecolor = "red", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )

);

#--------------------------------------------------------------------------

# Experiment four.

# Plot initial x-t, y-t to final x-t, y-t.

plt.plot( [ exp4_best_initial[ 0 ], exp4_best_final[ 0 ] ], [ exp4_best_initial[ 1 ], exp4_best_final[ 1 ] ], "--g", linewidth = 1 );

# Plot initial x-t, y-t.

plt.plot( [ exp4_best_initial[ 0 ] ], [ exp4_best_initial[ 1 ] ], "go", linewidth = 1 );

# Plot final x-y, y-t.

plt.plot( [ exp4_best_final[ 0 ] ], [ exp4_best_final[ 1 ] ], "go", linewidth = 1 );

# Initial orientation.

a1, b1 = rotate_point( arrow_size, 0.0, exp4_best_initial[ 5 ] );
		
a1 = exp4_best_initial[ 0 ] + a1;
b1 = exp4_best_initial[ 1 ] + b1;

plt.annotate( 

	"", 
	xy = ( a1, b1 ), 
	xytext = ( exp4_best_initial[ 0 ], exp4_best_initial[ 1 ] ),
	arrowprops = dict( facecolor = "green", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )

);

# Final orientation.

a1, b1 = rotate_point( arrow_size, 0.0, exp4_best_final[ 5 ] );
		
a1 = exp4_best_final[ 0 ] + a1;
b1 = exp4_best_final[ 1 ] + b1;

plt.annotate( 

	"", 
	xy = ( a1, b1 ), 
	xytext = ( exp4_best_final[ 0 ], exp4_best_final[ 1 ] ),
	arrowprops = dict( facecolor = "green", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )

);

#--------------------------------------------------------------------------

# Experiment five.

# Plot initial x-t, y-t to final x-t, y-t.

plt.plot( [ exp5_best_initial[ 0 ], exp5_best_final[ 0 ] ], [ exp5_best_initial[ 1 ], exp5_best_final[ 1 ] ], "--m", linewidth = 1 );

# Plot initial x-t, y-t.

plt.plot( [ exp5_best_initial[ 0 ] ], [ exp5_best_initial[ 1 ] ], "mo", linewidth = 1 );

# Plot final x-y, y-t.

plt.plot( [ exp5_best_final[ 0 ] ], [ exp5_best_final[ 1 ] ], "mo", linewidth = 1 );

# Initial orientation.

a1, b1 = rotate_point( arrow_size, 0.0, exp5_best_initial[ 5 ] );
		
a1 = exp5_best_initial[ 0 ] + a1;
b1 = exp5_best_initial[ 1 ] + b1;

plt.annotate( 

	"", 
	xy = ( a1, b1 ), 
	xytext = ( exp5_best_initial[ 0 ], exp5_best_initial[ 1 ] ),
	arrowprops = dict( facecolor = "magenta", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )

);

# Final orientation.

a1, b1 = rotate_point( arrow_size, 0.0, exp5_best_final[ 5 ] );
		
a1 = exp5_best_final[ 0 ] + a1;
b1 = exp5_best_final[ 1 ] + b1;

plt.annotate( 

	"", 
	xy = ( a1, b1 ), 
	xytext = ( exp5_best_final[ 0 ], exp5_best_final[ 1 ] ),
	arrowprops = dict( facecolor = "magenta", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )

);

#--------------------------------------------------------------------------

# Plot real robot centroid.

plt.plot( [ 0, real_robot_centroid_robust[ 0 ] ], [ 0, real_robot_centroid_robust[ 1 ] ], "--k", linewidth = 1 );

a1, b1 = rotate_point( arrow_size, 0.0, real_robot_centroid_robust[ 2 ] );
		
a1 = 0.0 + a1;
b1 = 0.0 + b1;

plt.annotate( 

	"", 
	xy = ( a1, b1 ), 
	xytext = ( 0.0, 0.0 ),
	arrowprops = dict( facecolor = "black", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )

);

# X-t and Y-t.

plt.plot( [ real_robot_centroid_robust[ 0 ] ], [ real_robot_centroid_robust[ 1 ] ], "ko", linewidth = 1 );

# Z-r

a1, b1 = rotate_point( arrow_size, 0.0, real_robot_centroid_robust[ 2 ] );
		
a1 = real_robot_centroid_robust[ 0 ] + a1;
b1 = real_robot_centroid_robust[ 1 ] + b1;

plt.annotate( 

	"", 
	xy = ( a1, b1 ), 
	xytext = ( real_robot_centroid_robust[ 0 ], real_robot_centroid_robust[ 1 ] ),
	arrowprops = dict( facecolor = "black", alpha = 0.5, frac = 0.5, width = 2, headwidth = 6  )

);

# Legend.
	
robust_mean = plt.Circle( ( 0, 0 ), 0.2, color = "k", alpha = 0.7 );

exp2 = plt.Circle( ( 0, 0 ), 0.2, color = "b", alpha = 0.7 );
exp3 = plt.Circle( ( 0, 0 ), 0.2, color = "r", alpha = 0.7 );
exp4 = plt.Circle( ( 0, 0 ), 0.2, color = "g", alpha = 0.7 );
exp5 = plt.Circle( ( 0, 0 ), 0.2, color = "m", alpha = 0.7 );
	
plt.legend( [ robust_mean, exp2, exp3, exp4, exp5 ], [ "Robust Mean", "Exp. Two", "Exp. Three", "Exp. Four", "Exp. Five" ] );

#--------------------------------------------------------------------------

# Begin plotting the 3D scatter plot comparison.

fig = plt.figure( 2, figsize = ( 12, 12 ) );
#ax  = fig.gca( projection = "3d" );
ax = fig.add_subplot( 111, projection = "3d" );

ax.set_title(  "BBAutoTune \n\n Simulated versus Real Motion", fontsize = 15 );
ax.set_xlabel( "X-position in Centimeters",                 fontsize = 15 );
ax.set_ylabel( "Y-position in Centimeters",                 fontsize = 15 );
ax.set_zlabel( "Heading in Radians",                        fontsize = 15, linespacing = 10 );

ax.plot( [ exp2_best_final[ 0 ], real_robot_centroid_robust[ 0 ] ], 
	 [ exp2_best_final[ 1 ], real_robot_centroid_robust[ 1 ] ], 
	 [ exp2_best_final[ 5 ], real_robot_centroid_robust[ 2 ] ], 
	 alpha = 0.5, color = "0.5", marker = "o", ms = 10 );

ax.plot( [ exp3_best_final[ 0 ], real_robot_centroid_robust[ 0 ] ], 
	 [ exp3_best_final[ 1 ], real_robot_centroid_robust[ 1 ] ], 
	 [ exp3_best_final[ 5 ], real_robot_centroid_robust[ 2 ] ], 
	 alpha = 0.5, color = "0.5", marker = "o", ms = 10 );

ax.plot( [ exp4_best_final[ 0 ], real_robot_centroid_robust[ 0 ] ], 
	 [ exp4_best_final[ 1 ], real_robot_centroid_robust[ 1 ] ], 
	 [ exp4_best_final[ 5 ], real_robot_centroid_robust[ 2 ] ], 
	 alpha = 0.5, color = "0.5", marker = "o", ms = 10 );

ax.plot( [ exp5_best_final[ 0 ], real_robot_centroid_robust[ 0 ] ], 
	 [ exp5_best_final[ 1 ], real_robot_centroid_robust[ 1 ] ], 
	 [ exp5_best_final[ 5 ], real_robot_centroid_robust[ 2 ] ], 
	 alpha = 0.5, color = "0.5", marker = "o", ms = 10 );

# Plot the real robot classic centroid.

#ax.plot( [ real_robot_centroid_classic[ 0 ] ], [ real_robot_centroid_classic[ 1 ] ], [ real_robot_centroid_classic[ 2 ] ], alpha = 0.5, c = "0.75", marker = "o", ms = 10 );

# Plot the real robot robust centroid.

ax.plot( [ real_robot_centroid_robust[ 0 ] ], [ real_robot_centroid_robust[ 1 ] ], [ real_robot_centroid_robust[ 2 ] ], alpha = 0.5, c = "k", marker = "o", ms = 10 );

# Plot the rest.

ax.plot( [ exp2_best_final[ 0 ] ], [ exp2_best_final[ 1 ] ], [ exp2_best_final[ 5 ] ], alpha = 0.5, c = "b", marker = "o", ms = 10 );
ax.plot( [ exp3_best_final[ 0 ] ], [ exp3_best_final[ 1 ] ], [ exp3_best_final[ 5 ] ], alpha = 0.5, c = "r", marker = "o", ms = 10 );
ax.plot( [ exp4_best_final[ 0 ] ], [ exp4_best_final[ 1 ] ], [ exp4_best_final[ 5 ] ], alpha = 0.5, c = "g", marker = "o", ms = 10 );
ax.plot( [ exp5_best_final[ 0 ] ], [ exp5_best_final[ 1 ] ], [ exp5_best_final[ 5 ] ], alpha = 0.5, c = "m", marker = "o", ms = 10 );

# Plot robust distances.

ax.text( real_robot_centroid_robust[ 0 ]  + 0.05, real_robot_centroid_robust[ 1 ], real_robot_centroid_robust[ 2 ], "RD=" + str( rrrd ), color = "black" );

ax.text( exp2_best_final[ 0 ]  + 0.05, exp2_best_final[ 1 ], exp2_best_final[ 5 ], "RD=" + str( exp2rd ), color = "blue"    );
ax.text( exp3_best_final[ 0 ]  + 0.05, exp3_best_final[ 1 ], exp3_best_final[ 5 ], "RD=" + str( exp3rd ), color = "red"     );
ax.text( exp4_best_final[ 0 ]  + 0.05, exp4_best_final[ 1 ], exp4_best_final[ 5 ], "RD=" + str( exp4rd ), color = "green"   );
ax.text( exp5_best_final[ 0 ]  + 0.05, exp5_best_final[ 1 ], exp5_best_final[ 5 ], "RD=" + str( exp5rd ), color = "magenta" );

for xtick in ax.xaxis.get_major_ticks( ):
	
	xtick.label.set_fontsize( 15 );
	
for ytick in ax.yaxis.get_major_ticks( ):

	ytick.label.set_fontsize( 15 );
	
for ztick in ax.zaxis.get_major_ticks( ):

	ztick.label.set_fontsize( 15 );
	
# Legend.
	
robust_mean = plt.Circle( ( 0, 0 ), 0.2, color = "k", alpha = 0.7 );

exp2 = plt.Circle( ( 0, 0 ), 0.2, color = "b", alpha = 0.7 );
exp3 = plt.Circle( ( 0, 0 ), 0.2, color = "r", alpha = 0.7 );
exp4 = plt.Circle( ( 0, 0 ), 0.2, color = "g", alpha = 0.7 );
exp5 = plt.Circle( ( 0, 0 ), 0.2, color = "m", alpha = 0.7 );
	
ax.legend( [ robust_mean, exp2, exp3, exp4, exp5 ], [ "Robust Mean", "Exp. Two", "Exp. Three", "Exp. Four", "Exp. Five" ] );

plt.subplots_adjust( left = 0.0, right = 1.0, top = 1.0, bottom = 0.0 );

plt.show( );

