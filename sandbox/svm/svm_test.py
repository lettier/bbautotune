import random;
import numpy;
import cPickle;

# Import real robot forward motion data.

x_p_values = cPickle.load( open( "x_p_values.pkl", "rb" ) );
y_p_values = cPickle.load( open( "y_p_values.pkl", "rb" ) );
t_p_values = cPickle.load( open( "t_p_values.pkl", "rb" ) );

from sklearn.svm import OneClassSVM;
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

ocsvm = OneClassSVM( kernel = "poly", degree = 4 );

# K-fold cross-validation.

prediction_scores = [ ];

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
	
	predictions = ocsvm.fit( a_train ).predict( a_test );
	
	number_right = 0;
	
	for p in predictions:
		
		if p == 1.0:
			
			number_right += 1;
	
	prediction_scores.append( float( number_right ) / float( len( predictions ) ) );
	
print "Prediction scores: ", prediction_scores;
	
print "Prediction score mean: ", sum( prediction_scores ) / float( len( prediction_scores ) );