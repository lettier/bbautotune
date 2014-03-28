import random;
import numpy;
import numpy.linalg;
import pickle;
import math;
import matplotlib.pyplot as plt;
import matplotlib.mlab as mlab;
from mpl_toolkits.mplot3d import Axes3D;
from matplotlib import cm;
from matplotlib.patches import Rectangle;
from scipy.stats import chi2;
import scipy.spatial.distance;
from scipy.stats import scoreatpercentile;
from scipy.stats import mode;
from scipy.stats import normaltest;
from scipy.stats import norm;
from scipy.stats import probplot;
from sklearn.covariance import EllipticEnvelope;
from sklearn.covariance import MinCovDet;
from sklearn.cross_validation import cross_val_score;
from sklearn.cross_validation import train_test_split;

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
	
# Data and its labels. 1 = forward.
	
forward_motion = numpy.array( forward_motion );
label          = numpy.array( [ 1 ]*len( forward_motion ) );

'''

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

'''

print "MCD: ";

mcd_trained = MinCovDet( assume_centered = False, support_fraction = 0.5 * ( len( forward_motion ) + 3.0 + 1.0 ) ).fit( forward_motion );

mcd_md2s = mcd_trained.dist_;

mds = [ ];

classical_mean = mcd_trained.raw_location_;

robust_mean = mcd_trained.location_;

classical_covariance_matrix_inverse = numpy.linalg.inv( mcd_trained.raw_covariance_ );

robust_covariance_matrix_inverse = numpy.linalg.inv( mcd_trained.covariance_ );

for i in range( len( forward_motion ) ):
	
	md = scipy.spatial.distance.mahalanobis( forward_motion[ i ], mcd_trained.location_, robust_covariance_matrix_inverse );
	
	mds.append( md );

print "Max MD: ", max( mds );
print "Min MD: ", min( mds );
print "Classical Mean (Location): ", mcd_trained.raw_location_;
print "Robust Mean (Location): ", mcd_trained.location_;
print "Classical Covariance Matrix: \n", mcd_trained.raw_covariance_;
print "Robust Covariance Matrix: \n", mcd_trained.covariance_;
print "Robust Mean (Location) MD: ", scipy.spatial.distance.mahalanobis( mcd_trained.location_, mcd_trained.location_, robust_covariance_matrix_inverse );
print "Classical Support samples: \n", mcd_trained.raw_support_;
print "Robust Support samples: \n", mcd_trained.support_;

robust_support_samples = [ ];

non_robust_support_samples = [ ];

for i in range( len( mcd_trained.support_ ) ):
	
	if ( mcd_trained.support_[ i ] == True ):
		
		robust_support_samples.append( forward_motion[ i ] );
		
	else:
		
		non_robust_support_samples.append( forward_motion[ i ] );
		
# Compare MD versus RD.

classical_md = [ ];
robust_md    = [ ];

for i in range( len( forward_motion ) ):
	
	md = scipy.spatial.distance.mahalanobis( forward_motion[ i ], mcd_trained.raw_location_, classical_covariance_matrix_inverse );
	
	classical_md.append( md );
	
	rd = scipy.spatial.distance.mahalanobis( forward_motion[ i ], mcd_trained.location_, robust_covariance_matrix_inverse );
	
	robust_md.append( rd );

md2s_sorted = sorted( map( lambda a: a * a, mds ) );

mds_sorted = sorted( mds );

chi2_quantiles = [ ];

for i in range( len( mds_sorted ) ):
	
	j = i + 1.0
	
	n = len( mds_sorted );
	
	q_j = ( j - 0.5 ) / n;
	
	x2 = chi2.isf( 1.0 - q_j, 3 );
	
	x2_sr = math.sqrt( x2 );
	
	chi2_quantiles.append( x2_sr );
	
# Plot 1.

plt.figure( 1 );
plt.scatter( chi2_quantiles, mds_sorted, color = "green", alpha = 0.5 );
plt.title( "Real Robot Forward Motion Q-Q Plot" );
plt.xlabel( "Square Root of Chi-square Probability Quantile" );
plt.ylabel( "Ordered Mahalanobis Distance Quantile" );
plt.plot( [ min( chi2_quantiles ), max( chi2_quantiles ) ], [ min( chi2_quantiles ), max( chi2_quantiles ) ], color = "red", alpha = 0.5 );
plt.plot( 

	[ 0, max( chi2_quantiles ) ],
	[ math.sqrt( chi2.isf( 1.0 - 0.995, 3 ) ), math.sqrt( chi2.isf( 1.0 - 0.995, 3 ) ) ],
	color = "blue", alpha = 0.5 
	
);
plt.grid( True );

# Plot 2.

plt.figure( 2 );

for i in range( len( mds ) ):
	
	if ( not ( ( mds[ i ] * mds[ i ] ) > chi2.isf( 1.0 - 0.995, 3 ) ) ):
		
		plt.plot( [ i + 1 ], [ mds[ i ] ], color = "blue", alpha = 0.5, marker = "o" );

for i in range( len( mds ) ):
		
	if ( ( mds[ i ] * mds[ i ] ) > chi2.isf( 1.0 - 0.995, 3 ) ):
		
		plt.plot( [ i + 1 ], [ mds[ i ] ], color = "red", alpha = 0.5, marker = "o" );

plt.title( "Real Robot Forward Motion Outliers" );
plt.ylabel( "Mahalanobis Distance" );
plt.xlabel( "Observation" );
plt.grid( True );
plt.ylim( bottom = -10.0, top = max( mds ) + 10 );
plt.xlim( left = -100.0 );

print "Outliers > 99.5% Chi-square critical value: ";

outlier_indexes = [ ];

j = 0;

for i in range( len( mds ) ):
	
	if ( ( mds[ i ] * mds[ i ] ) > chi2.isf( 1.0 - 0.995, 3 ) ):
		
		outlier_indexes.append( i );
		
		j += 1;
		
print "Number of outliers: ", j;
print "Percentage of outliers: {0:.0f}%".format( ( float( j ) / len( forward_motion ) ) * 100 );

# Plot 3.

# Graph support samples used to compute the robust mean and cov-mat.

fig = plt.figure( 3, figsize = ( 12, 12 ) );
ax  = fig.gca( projection = "3d" );

ax.grid( alpha = 1.0 );

ax.set_title(  "BBAutoTune \n\n Real Robot Forward Motion Robust Support Samples", fontsize = 15 );
ax.set_xlabel( "X-translation in Centimeters", fontsize = 15 );
ax.set_ylabel( "Y-translation in Centimeters", fontsize = 15 );
ax.set_zlabel( "Z-rotation in Radians",  fontsize = 15, linespacing = 10 );

for i in range( len( non_robust_support_samples ) ):
	
	ax.plot( 
		
		[ non_robust_support_samples[ i ][ 0 ] ], 
		[ non_robust_support_samples[ i ][ 1 ] ], 
		[ non_robust_support_samples[ i ][ 2 ] ], 
		color = "0.75", 
		marker = "o",
		alpha = 0.7,
		ms = 15 
		
	);
		
for i in range( len( robust_support_samples ) ):
		
	ax.plot( 
		
		[ robust_support_samples[ i ][ 0 ] ], 
		[ robust_support_samples[ i ][ 1 ] ], 
		[ robust_support_samples[ i ][ 2 ] ], 
		color = "b",
		alpha = 0.7,
		marker = "o", 
		ms = 15 
		
	);
	
plt.subplots_adjust( left = 0.0, right = 1.0, top = 1.0, bottom = 0.0 );

# Graph outliers.

'''

fig = plt.figure( 3, figsize = ( 12, 12 ) );
ax  = fig.gca( projection = "3d" );

ax.grid( alpha = 1.0 );

ax.set_title(  "Real Robot Forward Motion Outliers", fontsize = 15 );
ax.set_xlabel( "X-axis Delta in Centimeters", fontsize = 15 );
ax.set_ylabel( "Y-axis Delta in Centimeters", fontsize = 15 );
ax.set_zlabel( "Theta Delta in Radians",  fontsize = 15, linespacing = 10 );

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

'''

# Plot 4.

# Clean out the outliers.

forward_motion_clean = [ ];

for i in range( len( forward_motion ) ):
		
	if ( not i in outlier_indexes ):
		
		forward_motion_clean.append( [ forward_motion[ i ][ 0 ], forward_motion[ i ][ 1 ], forward_motion[ i ][ 2 ] ] );

forward_motion_clean = numpy.array( forward_motion_clean );

x_p_clean = [ ];
y_p_clean = [ ];
t_p_clean = [ ];

for i in range( len( forward_motion_clean ) ):
	
	x_p_clean.append( forward_motion_clean[ i ][ 0 ] );
	y_p_clean.append( forward_motion_clean[ i ][ 1 ] );
	t_p_clean.append( forward_motion_clean[ i ][ 2 ] );
	
x_p_mean = numpy.mean( x_p_clean );
y_p_mean = numpy.mean( y_p_clean );
t_p_mean = numpy.mean( t_p_clean );

x_p_var = numpy.var( x_p_clean );
y_p_var = numpy.var( y_p_clean );
t_p_var = numpy.var( t_p_clean );

x_p_std = numpy.std( x_p_clean );
y_p_std = numpy.std( y_p_clean );
t_p_std = numpy.std( t_p_clean );

x_p_median = numpy.median( x_p_clean );
y_p_median = numpy.median( y_p_clean );
t_p_median = numpy.median( t_p_clean );

x_p_mode = mode( x_p_clean );
y_p_mode = mode( y_p_clean );
t_p_mode = mode( t_p_clean );

z, x_p_normal_test = normaltest( x_p_clean, axis = 0 );
z, y_p_normal_test = normaltest( y_p_clean, axis = 0 );
z, t_p_normal_test = normaltest( t_p_clean, axis = 0 );

x_p_is_normal = "Normal";
y_p_is_normal = "Normal";
t_p_is_normal = "Normal";

if ( x_p_normal_test < 0.05 ):
	
	x_p_is_normal = "Not Normal";
	
if ( y_p_normal_test < 0.05 ):
	
	y_p_is_normal = "Not Normal";
	
if ( t_p_normal_test < 0.05 ):
	
	t_p_is_normal = "Not Normal";

print "Outliers gone.";

print "X' mean, median, mode: ", x_p_mean, x_p_median, x_p_mode[ 0 ][ 0 ];
print "Y' mean, median, mode: ", y_p_mean, y_p_median, y_p_mode[ 0 ][ 0 ];
print "T' mean, median, mode: ", t_p_mean, t_p_median, t_p_mode[ 0 ][ 0 ];

print "X' normal test p-value: ", x_p_normal_test, x_p_is_normal;
print "Y' normal test p-value: ", y_p_normal_test, y_p_is_normal;
print "T' normal test p-value: ", t_p_normal_test, t_p_is_normal;
	
# Calculate the Freedman-Diaconis' choice for bin size.
	
X_sorted = numpy.sort( x_p_clean );

Q3 = scoreatpercentile( X_sorted, 75 );
Q1 = scoreatpercentile( X_sorted, 25 );

IQR = Q3 - Q1;

h = 2.0 * ( IQR / ( len( X_sorted )**( 1.0 / 3.0 ) ) );

k_x = math.ceil( ( max( x_p_clean ) - min( x_p_clean ) ) / h );

plt.figure( 4 );

plt.subplot( 3, 1, 1 );
n, bins, patches = plt.hist( x_p_clean, bins = k_x, normed = True, alpha = 0.75, histtype = "stepfilled" );
max_patch_height = max( ( numpy.histogram( x_p_clean, k_x, normed = True ) )[ 0 ] );
normal_pdf       = mlab.normpdf( bins, x_p_mean, x_p_std );
plt.plot( bins, normal_pdf, "r--", linewidth = 1 );
current_axis = plt.gca( );
current_axis.add_patch( Rectangle( ( ( x_p_mean - x_p_std ), 0.0 ), x_p_std, max_patch_height, facecolor = "grey", alpha = 0.5 ) );
current_axis.add_patch( Rectangle( ( ( x_p_mean ), 0.0 ), x_p_std, max_patch_height, facecolor = "grey", alpha = 0.5 ) );
plt.plot( [ x_p_mean, x_p_mean ], [ 0.0, max_patch_height ], "g--", linewidth = 3 );
plt.plot( [ ( x_p_mean - x_p_std ), ( x_p_mean - x_p_std ) ], [ 0.0, max_patch_height ], "c--", linewidth = 3 );
plt.plot( [ ( x_p_mean + x_p_std ), ( x_p_mean + x_p_std ) ], [ 0.0, max_patch_height ], "c--", linewidth = 3 );
plt.plot( [ x_p_median, x_p_median ], [ 0.0, max_patch_height ], "k--", linewidth = 3 );
plt.title( "Real Robot Forward Motion w/out Outliers" );
plt.xlabel( "X-axis Delta in Centimeters" );
plt.ylabel( "PDF Normalized" );
plt.grid( True );

Y_sorted = numpy.sort( y_p_clean );

Q3 = scoreatpercentile( Y_sorted, 75 );
Q1 = scoreatpercentile( Y_sorted, 25 );

IQR = Q3 - Q1;

h = 2.0 * ( IQR / ( len( Y_sorted )**( 1.0 / 3.0 ) ) );

k_y = math.ceil( ( max( y_p_clean ) - min( y_p_clean ) ) / h );

plt.subplot( 3, 1, 2 );
n, bins, patches = plt.hist( y_p_clean, bins = k_y, normed = True, alpha = 0.75, histtype = "stepfilled" );
max_patch_height = max( ( numpy.histogram( y_p_clean, k_y, normed = True ) )[ 0 ] );
normal_pdf       = mlab.normpdf( bins, y_p_mean, y_p_std );
plt.plot( bins, normal_pdf, "r--", linewidth = 1 );
current_axis = plt.gca( );
current_axis.add_patch( Rectangle( ( ( y_p_mean - y_p_std ), 0.0 ), y_p_std, max_patch_height, facecolor = "grey", alpha = 0.5 ) );
current_axis.add_patch( Rectangle( ( ( y_p_mean ), 0.0 ), y_p_std, max_patch_height, facecolor = "grey", alpha = 0.5 ) );
plt.plot( [ y_p_mean, y_p_mean ], [ 0.0, max_patch_height ], "g--", linewidth = 3 );
plt.plot( [ ( y_p_mean - y_p_std ), ( y_p_mean - y_p_std ) ], [ 0.0, max_patch_height ], "c--", linewidth = 3 );
plt.plot( [ ( y_p_mean + y_p_std ), ( y_p_mean + y_p_std ) ], [ 0.0, max_patch_height ], "c--", linewidth = 3 );
plt.plot( [ y_p_median, y_p_median ], [ 0.0, max_patch_height ], "k--", linewidth = 3 );
plt.title( "Real Robot Forward Motion w/out Outliers" );
plt.xlabel( "Y-axis Delta in Centimeters" );
plt.ylabel( "PDF Normalized" );
plt.grid( True );

T_sorted = numpy.sort( t_p_clean );

Q3 = scoreatpercentile( T_sorted, 75 );
Q1 = scoreatpercentile( T_sorted, 25 );

IQR = Q3 - Q1;

h = 2.0 * ( IQR / ( len( T_sorted )**( 1.0 / 3.0 ) ) );

k_t = math.ceil( ( max( t_p_clean ) - min( t_p_clean ) ) / h );

plt.subplot( 3, 1, 3 );
n, bins, patches = plt.hist( t_p_clean, bins = k_t, normed = True, alpha = 0.75, histtype = "stepfilled" );
max_patch_height = max( ( numpy.histogram( t_p_clean, k_t, normed = True ) )[ 0 ] );
normal_pdf       = mlab.normpdf( bins, t_p_mean, t_p_std );
plt.plot( bins, normal_pdf, "r--", linewidth = 1 );
current_axis = plt.gca( );
current_axis.add_patch( Rectangle( ( ( t_p_mean - t_p_std ), 0.0 ), t_p_std, max_patch_height, facecolor = "grey", alpha = 0.5 ) );
current_axis.add_patch( Rectangle( ( ( t_p_mean ), 0.0 ), t_p_std, max_patch_height, facecolor = "grey", alpha = 0.5 ) );
plt.plot( [ t_p_mean, t_p_mean ], [ 0.0, max_patch_height ], "g--", linewidth = 3 );
plt.plot( [ ( t_p_mean - t_p_std ), ( t_p_mean - t_p_std ) ], [ 0.0, max_patch_height ], "c--", linewidth = 3 );
plt.plot( [ ( t_p_mean + t_p_std ), ( t_p_mean + t_p_std ) ], [ 0.0, max_patch_height ], "c--", linewidth = 3 );
plt.plot( [ t_p_median, t_p_median ], [ 0.0, max_patch_height ], "k--", linewidth = 3 );
plt.title( "Real Robot Forward Motion w/out Outliers" );
plt.xlabel( "Theta Delta in Degrees" );
plt.ylabel( "PDF Normalized" );
plt.grid( True );

plt.tight_layout( pad = 1.08, h_pad = 0.5 );

# Plot 5.

plt.figure( 5 );

plt.subplot( 3, 1, 1 );
n, bins, patches = plt.hist( x_p_clean, bins = k_x, normed = True, alpha = 0.75, cumulative = True, histtype = "stepfilled" );
normal_data = sorted( norm.rvs( size = len( x_p_clean ), loc = x_p_mean, scale = x_p_std ) );
normal_data_cdf = norm.cdf( normal_data, x_p_mean, x_p_std );
plt.plot( normal_data, normal_data_cdf, "--r" );
plt.title( "Real Robot Forward Motion w/out Outliers" );
plt.xlabel( "X-axis Delta in Centimeters" );
plt.ylabel( "CDF Normalized" );
plt.grid( True );

plt.subplot( 3, 1, 2 );
plt.hist( y_p_clean, bins = k_y, normed = True, alpha = 0.75, cumulative = True, histtype = "stepfilled" );
normal_data = sorted( norm.rvs( size = len( y_p_clean ), loc = y_p_mean, scale = y_p_std ) );
normal_data_cdf = norm.cdf( normal_data, y_p_mean, y_p_std );
plt.plot( normal_data, normal_data_cdf, "--r" );
plt.title( "Real Robot Forward Motion w/out Outliers" );
plt.xlabel( "Y-axis Delta in Centimeters" );
plt.ylabel( "CDF Normalized" );
plt.grid( True );

plt.subplot( 3, 1, 3 );
plt.hist( t_p_clean, bins = k_t, normed = True, alpha = 0.75, cumulative = True, histtype = "stepfilled" );
normal_data = sorted( norm.rvs( size = len( t_p_clean ), loc = t_p_mean, scale = t_p_std ) );
normal_data_cdf = norm.cdf( normal_data, t_p_mean, t_p_std );
plt.plot( normal_data, normal_data_cdf, "--r" );
plt.title( "Real Robot Forward Motion w/out Outliers" );
plt.xlabel( "Theta Delta in Degrees" );
plt.ylabel( "CDF Normalized" );
plt.grid( True );

plt.tight_layout( pad = 1.08, h_pad = 0.5 );

# Plot 6.

mds_clean = map( lambda a: scipy.spatial.distance.mahalanobis( a, mcd_trained.location_, robust_covariance_matrix_inverse ), forward_motion_clean )

print "Max MD: ", max( mds_clean );
print "Min MD: ", min( mds_clean );
	
md2s_clean_sorted = sorted( map( lambda a: a * a, mds_clean ) );

mds_clean_sorted = sorted( mds_clean )

chi2_quantiles = [ ];

for i in range( len( mds_clean_sorted ) ):
	
	j = i + 1.0
	
	n = len( mds_clean_sorted );
	
	q_j = ( j - 0.5 ) / n;
	
	x2 = chi2.isf( 1.0 - q_j, 3 );
	
	x2_sr = math.sqrt( x2 );
	
	chi2_quantiles.append( x2_sr );

plt.figure( 6 );
plt.scatter( chi2_quantiles, mds_clean_sorted, color = "green", alpha = 0.5 );
plt.title( "Real Robot Forward Motion Q-Q Plot w/out Outliers" );
plt.xlabel( "Square Root of Chi-square Probability Quantile" );
plt.ylabel( "Ordered Mahalanobis Distance Quantile" );
plt.plot( [ min( chi2_quantiles ), max( chi2_quantiles ) ], [ min( chi2_quantiles ), max( chi2_quantiles ) ], color = "red", alpha = 0.5 );
plt.plot( 
	
	[ 0, max( chi2_quantiles ) ], 
	[ math.sqrt( chi2.isf( 1.0 - 0.995, 3 ) ), math.sqrt( chi2.isf( 1.0 - 0.995, 3 ) ) ], 
	color = "blue", alpha = 0.5 
	
);
plt.grid( True );

# Plot 7.

plt.figure( 7 );

plt.subplot( 3, 1, 1 );
plt.grid( True );
x_qq_plot = probplot( x_p_clean, dist = "norm", sparams = ( x_p_mean, x_p_std ), plot = plt );
plt.title( "Real Robot Forward Motion Q-Q Plot w/out Outliers" );
plt.xlabel( "Normal Quantile" );
plt.ylabel( "Ordered X-axis Delta Quantile" );

plt.subplot( 3, 1, 2 );
plt.grid( True );
x_qq_plot = probplot( y_p_clean, dist = "norm", sparams = ( y_p_mean, y_p_std ), plot = plt );
plt.title( "Real Robot Forward Motion Q-Q Plot w/out Outliers" );
plt.xlabel( "Normal Quantile" );
plt.ylabel( "Ordered Y-axis Delta Quantile" );

plt.subplot( 3, 1, 3 );
plt.grid( True );
x_qq_plot = probplot( t_p_clean, dist = "norm", sparams = ( t_p_mean, t_p_std ), plot = plt );
plt.title( "Real Robot Forward Motion Q-Q Plot w/out Outliers" );
plt.xlabel( "Normal Quantile" );
plt.ylabel( "Ordered Theta Delta Quantile" );

# Plot 8.

plt.figure( 8 );

plt.grid( True );

plt.scatter( classical_md, robust_md, color = "green", alpha = 0.5 );
plt.title( "BBAutoTune \n\n Real Robot Forward Motion MD versus RD" );
plt.xlabel( "Mahalanobis Distance (MD)" );
plt.ylabel( "Robust Distance (RD)" );
plt.plot( [ min( classical_md ), max( classical_md ) ], [ min( classical_md ), max( classical_md ) ], color = "red", alpha = 0.5 );


# Try the elliptical envelope now with the outliers gone.

print "EE:";

ssp = numpy.array( [ [ -10, 25.0, 0.0 ] ] );

print "Sample simulated point [[X',Y',T']]: ", ssp;

ee = EllipticEnvelope( assume_centered = False, contamination = 0.0 );

print "With outliers:";

print "In envelope? ", ee.fit( forward_motion ).predict( ssp );
print "MD: ", math.sqrt( ee.fit( forward_motion ).mahalanobis( ssp ) );

print "Without outliers:";

print "In envelope? ", ee.fit( forward_motion_clean ).predict( ssp );
print "MD: ", math.sqrt( ee.fit( forward_motion_clean ).mahalanobis( ssp ) );

# Show the plots.

plt.show( );
