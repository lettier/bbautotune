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

# Rotates a point around the origin, counter-clockwise.

def rotate_point( x, y, angle_r ):
	
	x_rot = ( math.cos( angle_r ) * x ) + ( -math.sin( angle_r ) * y );
	y_rot = ( math.sin( angle_r ) * x ) + (  math.cos( angle_r ) * y );
	
	return x_rot, y_rot;

# real_robot_centroid = [ 23.8644631679, 0.338269853117, -0.00417473025048 ]; # Classical mean.

real_robot_centroid = [ 23.9934044, 0.0351240536, -0.0189964938 ]; # Robust mean.

plt.figure( 1 );

plt.title( "BBAutoTune \n\n Simulated Motion versus Real Motion" );
plt.ylabel( "Y-translation" );
plt.xlabel( "X-translation" );
plt.grid( True );
plt.axis( "equal" );

arrow_size = 0.5;

#--------------------------------------------------------------------------

# Experiment two.

exp2_best_initial = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ];
exp2_best_final   = [ 23.123499751091003, .009536895231576636, 0.0, 0.0, -0.0, 0.002033736789599061 ];

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

exp3_best_initial = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ];
exp3_best_final   = [ 23.95108938217163, -0.3489761846140027, 0.0, 0.0, 0.0, -0.00318596581928432 ];

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

exp4_best_initial = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ];
exp4_best_final   = [ 23.491448163986206, -0.002863347253878601, 0.0, 0.0 ,0.0, -0.004287547431886196 ];

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

