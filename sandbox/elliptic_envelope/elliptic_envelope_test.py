import random;
import numpy;
import cPickle;
import math;
import matplotlib.pyplot as plt;
import matplotlib.mlab as mlab;
from mpl_toolkits.mplot3d import Axes3D;
from matplotlib import cm;
from matplotlib.patches import Rectangle;

# Import real robot forward motion data.

x_p_values = cPickle.load( open( "x_p_values.pkl", "rb" ) );
y_p_values = cPickle.load( open( "y_p_values.pkl", "rb" ) );
t_p_values = cPickle.load( open( "t_p_values.pkl", "rb" ) );
	
from sklearn.covariance import EllipticEnvelope;
from sklearn.covariance import MinCovDet;
from sklearn.cross_validation import cross_val_score;
from sklearn.cross_validation import train_test_split;

forward_motion = [ ];

for i in range( len( x_p_values ) ):
	
	x_p_value = x_p_values[ i ];
	y_p_value = y_p_values[ i ];
	t_p_value = t_p_values[ i ];
	
	forward_motion.append( 
		
		[ x_p_value, y_p_value, t_p_value ]
		
	);
	
# Data and its labels. 1 = forward.
	
forward_motion = numpy.array( forward_motion );
label          = numpy.array( [ 1 ]*len( forward_motion ) );

# Classifier.

ee = EllipticEnvelope( assume_centered = False, contamination = 0.0 );

# K-fold cross-validation.

prediction_scores = [ ];

mds = [ ];

k = 10

# Round returns incorrect values but converting its return value to a string does return the right value.
# Convert only the numbers before the decimal '.' to an integer.

chunk_size = int( str( round( float( len( forward_motion ) ) / k ) ).split( "." )[ 0 ] );

for i in range( 0, k ):
	
	print "Fold: ", i + 1;
	
	test_start =  i * chunk_size;
	test_stop  = chunk_size * ( i + 1 );
	
	if ( test_stop >= len( forward_motion ) ):
		
		test_stop = test_stop - ( test_stop - len( forward_motion ) );
	
	train_start1 = 0;
	train_stop1  = None;
	
	if ( test_stop == len( forward_motion ) ):
		
		train_stop1 = test_start;
	
	else:
		
		train_stop1  = test_stop - chunk_size;
		
	train_start2 = test_stop;
	train_stop2  = len( forward_motion );

	a_train = None;
	b_train = None;
	
	if ( train_stop1 == 0 ):
		
		a_train = forward_motion[ train_start2 : train_stop2 ];
		b_train = label[ train_start2 : train_stop2 ];
		
		print "Test: [", test_start, ":", test_stop, "] ", " Train: [", train_start2, ":", train_stop2, "]";

		
	elif ( train_start2 == len( forward_motion ) ):
		
		a_train = forward_motion[ train_start1 : train_stop1 ];
		b_train = label[ train_start1 : train_stop1 ];
		
		print "Train: [", train_start1, ":", train_stop1, "] ", " Test: [", test_start, ":", test_stop, "]";
		
	else:
	
		a_train = numpy.concatenate( 
			
			( forward_motion[ train_start1 : train_stop1 ], 
			  forward_motion[ train_start2 : train_stop2 ] )
		); 
				
		b_train = numpy.concatenate( 
			
			( label[ train_start1 : train_stop1 ],
			  label[ train_start2 : train_stop2 ] )
			
		);
		
		print "Train: [", train_start1, ":", train_stop1, "] +", "[", train_start2, ":", train_stop2, "]", " Test: [", test_start, ":", test_stop, "]";

	a_test = forward_motion[ test_start : test_stop ];
	b_test = label[ test_start : test_stop ];
	
	ee_trained = ee.fit( a_train, b_train );
	
	prediction_scores.append( ee_trained.score( a_test, b_test ) );
	
	mds.extend( ee_trained.mahalanobis( a_test ) );
	
print "Prediction scores: ", prediction_scores;
	
print "Prediction score mean: ", sum( prediction_scores ) / float( len( prediction_scores ) );

print "Highest mahalanobis distance: ", max( mds );

print "Lowest mahalanobis distance: ", min( mds );

print ee.fit( forward_motion ).contamination;
print ee.fit( forward_motion ).covariance_;
print ee.fit( forward_motion ).location_;
print ee.fit( forward_motion ).precision_;
print ee.fit( forward_motion ).support_;

data_mask = ee.fit( forward_motion ).support_;

print "Potential outliers: ";

for i in range( len( data_mask ) ):
	
	if ( data_mask[ i ] == False ):
		
		print forward_motion[ i ];
		
mds = ee.fit( forward_motion ).mahalanobis( forward_motion );

print "Max/min mahalanobis distances: ";

print max( mds );
print min( mds );

ssp = numpy.array( [ [ 0.0, 25.0, 0.0 ] ] );

print "Sample simulated point: ", ssp;

print ee.fit( forward_motion ).predict(     ssp );
print ee.fit( forward_motion ).mahalanobis( ssp );

print "MCD: ";

mcd_trained = MinCovDet( assume_centered = False, support_fraction = 0.95 ).fit( forward_motion );

print mcd_trained.location_
print mcd_trained.raw_covariance_;
print mcd_trained.covariance_;
mcd_mds = mcd_trained.dist_;

print "Mahalanobis distances: ";
print mcd_mds;

print "Outliers > 95% Chi-square critical value : ";

outlier_indexes = [ ];

j = 0;

for i in range( len( mcd_mds ) ):
	
	if ( mcd_mds[ i ] > 7.815 ):
		
		print forward_motion[ i ];
		
		outlier_indexes.append( i );
		
		j += 1;
		
print "Number of outliers: ", j;
print "Percentage of outliers: {0:.0f}%".format( ( float( j ) / len( forward_motion ) ) * 100 );

print "Max/min mahalanobis distances: ";

print max( mcd_mds );
print min( mcd_mds );



# Graph outliers.

fig = plt.figure( 5, figsize = ( 12, 12 ) );
ax  = fig.gca( projection = "3d" );

ax.grid( alpha = 1.0 );

ax.set_title(  "Real Robot Forward Motion Outliers",   fontsize = 15 );
ax.set_xlabel( "X-axis Delta in Centimeters", fontsize = 15 );
ax.set_ylabel( "Y-axis Delta in Centimeters", fontsize = 15 );
ax.set_zlabel( "\nTheta Delta in Degrees\n",  fontsize = 15, linespacing = 10 );

for i in range( len( x_p_values ) ):
	
	if ( i in outlier_indexes ):
	
		ax.plot( 
			
			[ x_p_values[ i ] ], 
			[ y_p_values[ i ] ], 
			[ t_p_values[ i ] ], 
			color = "r", 
			marker = "o",
			alpha = 0.7,
			ms = 15 
			
		);
		
for i in range( len( x_p_values ) ):
		
	if ( not i in outlier_indexes ):
		
		ax.plot( 
			
			[ x_p_values[ i ] ], 
			[ y_p_values[ i ] ], 
			[ t_p_values[ i ] ], 
			color = "b",
			alpha = 0.7,
			marker = "o", 
			ms = 15 
			
		);
		
plt.subplots_adjust( left = 0.0, right = 1.0, top = 1.0, bottom = 0.0 );

plt.show( );

# Try the elliptical envelope now with the outliers gone.

forward_motion_clean = [ ];

for i in range( len( x_p_values ) ):
		
	if ( not i in outlier_indexes ):
		
		forward_motion_clean.append( [ x_p_values[ i ], y_p_values[ i ], t_p_values[ i ] ] );

forward_motion_clean = numpy.array( forward_motion_clean );

print "Outliers gone."

ssp = numpy.array( [ [ 0.0, 25.0, 0.0 ] ] );

print "Sample simulated point: ", ssp;

print ee.fit( forward_motion_clean ).predict(     ssp );
print ee.fit( forward_motion_clean ).mahalanobis( ssp );
		







