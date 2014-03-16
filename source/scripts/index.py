#!/usr/bin/env python

import MySQLdb as mdb;
import sys;
import numpy;

variables_location = "./variables/";
		
database_file = open( variables_location + "database.var", "r" );

user_name = database_file.readline( ).rstrip( );

password  = database_file.readline( ).rstrip( );

db_connection = mdb.connect( 'localhost', user_name, password, 'bbautotune' );

db_cursor = db_connection.cursor( );

db_cursor.execute( "SELECT * FROM  `population_metrics` LIMIT 0, 1000" );

result = db_cursor.fetchall( );

highest_fitnesses = [ ];
average_fitnesses = [ ];
lowest_fitnesses  = [ ];
crossover_probabilities = [ ];
mutation_probabilities = [ ];

for row in result:
	
	highest_fitnesses.append( row[ 2 ] );
	
	average_fitnesses.append( row[ 3 ] );
		
	lowest_fitnesses.append( row[ 4 ] );
	
	crossover_probabilities.append( row[ 5 ] );
	
	mutation_probabilities.append( row[ 6 ] );
	
if ( len( highest_fitnesses ) != 0 ):
	
	max_fitness = min( highest_fitnesses );
	min_fitness = max( lowest_fitnesses  );

	if ( min_fitness > 200.0 ):
		
		min_fitness = 200.0;
		
	hf_max  = min( highest_fitnesses );
	hf_min  = max( highest_fitnesses );
	hf_mean = numpy.mean( highest_fitnesses );
	hf_var  = numpy.var( highest_fitnesses );
	hf_std  = numpy.std( highest_fitnesses );

	af_max  = min( average_fitnesses );
	af_min  = max( average_fitnesses );
	af_mean = numpy.mean( average_fitnesses );
	af_var  = numpy.var( average_fitnesses );
	af_std  = numpy.std( average_fitnesses );

	lf_max  = min( lowest_fitnesses );
	lf_min  = max( lowest_fitnesses  );
	lf_mean = numpy.mean( lowest_fitnesses );
	lf_var  = numpy.var( lowest_fitnesses );
	lf_std  = numpy.std( lowest_fitnesses );
	
else:
	
	max_fitness = 0.0;
	min_fitness = 0.0;
	
	hf_max  = 0.0;
	hf_min  = 0.0;
	hf_mean = 0.0;
	hf_var  = 0.0;
	hf_std  = 0.0;

	af_max  = 0.0;
	af_min  = 0.0;
	af_mean = 0.0;
	af_var  = 0.0;
	af_std  = 0.0;

	lf_max  = 0.0;
	lf_min  = 0.0;
	lf_mean = 0.0;
	lf_var  = 0.0;
	lf_std  = 0.0;

print( "Content-type: text/html\n" );

print( "<!DOCTYPE html>" );
print( "<html>" );
print( "<head>" );
print( "<meta http-equiv='content-type' content='text/html; charset=UTF-8'>");
print( "<title>GA Progress Monitor | BBAutoTune</title>" );
print( "<script type='text/javascript' src='dependencies/Chart.min.js'></script>" );
print( "</head>" );
print( "<body style='background: #556;'>" );
print( "<font style='font-family: sans-serif; font-size: 50px; color: #fff;'>GA Progress Monitor | BBAutoTune</font><br><br>" );
print( "<table cellpadding='0' cellspacing='20px'>" );
print( "<tr>" );
print( "<td>" );
print( "<font style='font-family: sans-serif; font-size: 30px; color: #fff;'>GA Fitness Progress:&nbsp;</font>" );
print( "<font style='font-family: sans-serif; font-size: 20px; color: rgba( 255,  10,  10, 0.8 );'>Highest&nbsp;</font>" );
print( "<font style='font-family: sans-serif; font-size: 20px; color: rgba(  10, 255,  10, 0.8 );'>Average&nbsp;</font>" );
print( "<font style='font-family: sans-serif; font-size: 20px; color: rgba(  10,  10, 255, 0.8 );'>Lowest&nbsp;</font><br><br>" );
print( "<canvas id='fitness_chart' width='1500' height='600' style='background: #fff; border: 1px #000 solid;'></canvas>" );
print( "<script type='text/javascript'>" );
print( "document.getElementById('fitness_chart').width  = window.innerWidth - 100;" );
print( "document.getElementById('fitness_chart').height = window.innerHeight / 2;" );
print( "</script>" );
print( "</td>" );
print( "</tr>" );
print( "<tr>" );
print( "<td>" );
print( "<font style='font-family: sans-serif; font-size: 12px; color: #fff;'>Highest Fitness Max, Min, Mean, Variance, Standard Deviation: " + str( hf_max ) + ", " + str( hf_min ) + ", " + str( hf_mean ) + ", " + str( hf_var ) + ", " + str( hf_std ) + "</font><br>" );
print( "<font style='font-family: sans-serif; font-size: 12px; color: #fff;'>Average Fitness Max, Min, Mean, Variance, Standard Deviation: " + str( af_max ) + ", " + str( af_min ) + ", " + str( af_mean ) + ", " + str( af_var ) + ", " + str( af_std ) + "</font><br>" );
print( "<font style='font-family: sans-serif; font-size: 12px; color: #fff;'>Lowest Fitness Max, Min, Mean, Variance, Standard Deviation: "  + str( lf_max ) + ", " + str( lf_min ) + ", " + str( lf_mean ) + ", " + str( lf_var ) + ", " + str( lf_std ) + "</font><br>"  );
print( "</td>" );
print( "</tr>" );
print( "<tr>" );
print( "<td>" );
print( "<font style='font-family: sans-serif; font-size: 30px; color: rgba( 255, 10,  10, 0.8 );'>Crossover&nbsp;</font>" );
print( "<font style='font-family: sans-serif; font-size: 30px; color: #fff;'>&&nbsp;</font>" );
print( "<font style='font-family: sans-serif; font-size: 30px; color: rgba(  10, 255, 10, 0.8 );'>Mutation&nbsp;</font>" );
print( "<font style='font-family: sans-serif; font-size: 30px; color: #fff;'> Rate Progress:&nbsp;</font><br><br>" );
print( "<canvas id='cross_mut_chart' width='1500' height='600' style='background: #fff; border: 1px #000 solid;'></canvas>" );
print( "<script type='text/javascript'>" );
print( "document.getElementById('cross_mut_chart').width  = window.innerWidth - 100;" );
print( "document.getElementById('cross_mut_chart').height = window.innerHeight / 2;" );
print( "</script>" );
print( "</td>" );
print( "</tr>" );
print( "</table>" );
print( "<script type='text/javascript'>" );
print( "setTimeout( function ( ) { window.location.reload( false ); }, 60000 );" );
print( "var fitness_chart_context = document.getElementById( 'fitness_chart' ).getContext( '2d' );" );
print( "var fitness_data = {" );
print( "labels: [ " );

for row in result:
	
	print( "'" + str( row[ 1 ] ) + "'," ); # Generation number.

print( "]," );
print( "datasets: [" );
print( "{" );
print( "fillColor :   'rgba( 255, 10, 10, 0.09 )'," );
print( "strokeColor : 'rgba( 255, 10, 10, 0.8 )',"  );
print( "pointColor :  'rgba( 255, 10, 10, 0.5 )',"  );
print( "pointStrokeColor : '#911'," );
print( "data: [" );

for row in result:
	
	print( "'" + str( row[ 2 ] ) + "'," ); # Highest fitness.

print( "]" );
print( "}," );
print( "{" );
print( "fillColor :   'rgba( 10, 255, 10, 0.09 )'," );
print( "strokeColor : 'rgba( 10, 255, 10, 0.8 )',"  );
print( "pointColor :  'rgba( 10, 255, 10, 0.5 )',"  );
print( "pointStrokeColor : '#191'," );
print( "data: [" );

for row in result:
	
	print( "'" + str( row[ 3 ] ) + "'," ); # Average fitness. 

print( "]" );
print( "}," );
print( "{" );
print( "fillColor :   'rgba( 10, 10, 255, 0.09 )'," );
print( "strokeColor : 'rgba( 10, 10, 255, 0.8 )',"  );
print( "pointColor :  'rgba( 10, 10, 255, 0.5 )',"  );
print( "pointStrokeColor : '#119'," );
print( "data: [" );

for row in result:
	
	print( "'" + str( row[ 4 ] ) + "'," ); # Lowest fitness.

print( "]" );
print( "}" );
print( "]" );
print( "};" );
print( "var fitness_chart_options = { scaleOverride: true, scaleSteps: 20.1, scaleStepWidth: " + str( ( max_fitness - min_fitness ) / 20.0 ) + ", scaleStartValue: " + str( min_fitness ) + ", scaleFontFamily: \"'sans-serif'\" };" );
print( "var fitness_chart = new Chart( fitness_chart_context ).Line( fitness_data, fitness_chart_options );" );
print( "var cross_mut_chart_context = document.getElementById( 'cross_mut_chart' ).getContext( '2d' );" );
print( "var cross_mut_data = {" );
print( "labels: [ " );

for row in result:
	
	print( "'" + str( row[ 1 ] ) + "'," );

print( "]," );
print( "datasets: [" );
print( "{" );
print( "fillColor :   'rgba( 255, 10, 10, 0.1 )'," );
print( "strokeColor : 'rgba( 255, 10, 10, 0.8 )'," );
print( "pointColor :  'rgba( 255, 10, 10, 0.5 )'," );
print( "pointStrokeColor : '#333'," );
print( "data: [" );

for row in result:
	
	print( "'" + str( row[ 5 ] ) + "'," ); # Crossover probability.

print( "]" );
print( "}," );
print( "{" );
print( "fillColor :   'rgba( 10, 255, 10, 0.1 )'," );
print( "strokeColor : 'rgba( 10, 255, 10, 0.8 )'," );
print( "pointColor :  'rgba( 10, 255, 10, 0.5 )'," );
print( "pointStrokeColor : '#222'," );
print( "data: [" );

for row in result:
	
	print( "'" + str( row[ 6 ] ) + "'," ); # Mutation probability.

print( "]" );
print( "}" );
print( "]" );
print( "};" );
print( "var cross_mut_chart_options = { scaleOverride: true, scaleSteps: 20.1, scaleStepWidth: 0.05, scaleStartValue: 0.0, scaleFontFamily: \"'sans-serif'\" };" );
print( "var fitness_chart = new Chart( cross_mut_chart_context ).Line( cross_mut_data, cross_mut_chart_options );" );
print( "</script>" );
print( "<font style='font-family: sans-serif; font-size: 10px; color: #fff;'>David Lettier (C) 2014.</font><br><br>" );
print( "</body>" );
print( "</html>" );