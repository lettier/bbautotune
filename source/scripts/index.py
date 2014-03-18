#!/usr/bin/env python

import MySQLdb as mdb;
import sys;
import numpy;
import math;

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
	min_fitness = max( lowest_fitnesses );
	
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
	
	cp_max  = max( crossover_probabilities );	
	cp_min  = min( crossover_probabilities );
	
	mp_max  = max( mutation_probabilities );
	mp_min  = min( mutation_probabilities );
	
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
	
	cp_max  = 0.0;	
	cp_min  = 0.0;
	
	mp_max  = 0.0;
	mp_min  = 0.0;
	
yMax = 0.0;
yMin = 250.0;

print( "Content-type: text/html\n" );

print( "<!DOCTYPE html>" );
print( "<html>" );
print( "<head>" );
print( "<meta http-equiv='content-type' content='text/html; charset=UTF-8'>");
print( "<title>GA Progress Monitor | BBAutoTune</title>" );
print( "</head>" );
print( "<body style='background: #556; font-family: sans-serif; font-size: 15px; color: #fff;'>" );
print( "<font style='font-family: sans-serif; font-size: 50px; color: #fff;'>GA Progress Monitor | BBAutoTune</font><br><br>" );
print( "<table cellpadding='0' cellspacing='20px'>" );
print( "<tr>" );
print( "<td>" );
print( "<font style='font-family: sans-serif; font-size: 30px; color: #fff;'>Generation Fitness Progress:&nbsp;</font>" );
print( "<font id='highest_text' style='font-family: sans-serif; font-size: 20px; color: #89bbd8; cursor: pointer;'>Highest&nbsp;</font>" );
print( "<font id='average_text' style='font-family: sans-serif; font-size: 20px; color: #9dd597; cursor: pointer;'>Average&nbsp;</font>" );
print( "<font id='lowest_text'  style='font-family: sans-serif; font-size: 20px; color: #DD5C5C; cursor: pointer;'>Lowest&nbsp;</font>" );
print( "<font id='all_text'  style='font-family: sans-serif; font-size: 20px; color: #fff; cursor: pointer;'>ALL&nbsp;</font><br><br>" );
print( "<figure style='width: 800px; height: 600px;' id='fitnesses'></figure><br>" );
print( "</td>" );
print( "</tr>" );
print( "<tr>" );
print( "<td>" );
print( "<table cellspacing='15px'>" );
print( "<tr><td></td><td>Min</td><td>Max</td><td>Mean</td><td>Variance</td><td>Standard Deviation</td></tr>" );
print( "<tr><td><font style='font-family: sans-serif; font-size: 15px; color: #fff;'>Highest Fitness</font></td><td>" + str( hf_max ) + "</td><td>" + str( hf_min ) + "</td><td>" + str( hf_mean ) + "</td><td>" + str( hf_var ) + "</td><td>" + str( hf_std ) + "</td></tr>" );
print( "<tr><td><font style='font-family: sans-serif; font-size: 15px; color: #fff;'>Average Fitness</font></td><td>" + str( af_max ) + "</td><td>" + str( af_min ) + "</td><td>" + str( af_mean ) + "</td><td>" + str( af_var ) + "</td><td>" + str( af_std ) + "</td></tr>" );
print( "<tr><td><font style='font-family: sans-serif; font-size: 15px; color: #fff;'>Lowest Fitness</font></td><td>" + str( lf_max ) + "</td><td>" + str( lf_min ) + "</td><td>" + str( lf_mean ) + "</td><td>" + str( lf_var ) + "</td><td>" + str( lf_std ) + "</td></tr>"  );
print( "</table>" );
print( "</td>" );
print( "</tr>" );
print( "<tr>" );
print( "<td>" );
print( "<font style='font-family: sans-serif; font-size: 30px; color: #89bbd8;'>Crossover&nbsp;</font>" );
print( "<font style='font-family: sans-serif; font-size: 30px; color: #fff;'>&&nbsp;</font>" );
print( "<font style='font-family: sans-serif; font-size: 30px; color: #9dd597;'>Mutation&nbsp;</font>" );
print( "<font style='font-family: sans-serif; font-size: 30px; color: #fff;'> Rate Progress:&nbsp;</font><br><br>" );
print( "<figure style='width: 800px; height: 600px;' id='probabilities'></figure>" );
print( "</td>" );
print( "</tr>" );
print( "</table>" );
print( "<script type='text/javascript' src='dependencies/d3/d3.min.js'></script>" );
print( "<script type='text/javascript' src='dependencies/xcharts/xcharts.min.js'></script>" );
print( "<link rel='stylesheet' type='text/css' href='dependencies/xcharts/xcharts.css'>" );
print( "<script>" );
print( "document.getElementById('fitnesses').style.width  = window.innerWidth - 200 + 'px';" );
print( "document.getElementById('fitnesses').style.height = window.innerHeight -300 + 'px';" );
print( " var fitnesses_data = { 'xScale': 'linear', 'yScale': 'exponential', 'yMax': " + str( hf_max ) +", 'yMin': " + str( lf_min ) + ", 'xMax': " + str( len( highest_fitnesses ) - 1 ) + ", 'xMin': 0, 'main': [ " );
print( "{ 'className': '.highFitnesses', 'data': [" );

for i in range( len( highest_fitnesses ) ):
	
	print( "{" );
	print( "'x':" + str( i ) + "," );
	print( "'y':" + str( highest_fitnesses[ i ] ) );
	print( "}," );
	
print( "] }," );
print( "{ 'className': '.averageFitnesses', 'data': [" );
for i in range( len( average_fitnesses ) ):
	
	print( "{" );
	print( "'x':" + str( i ) + "," );
	print( "'y':" + str( average_fitnesses[ i ] ) );
	print( "}," );
print( " ] }," );
print( "{ 'className': '.lowestFitnesses', 'data': [" );
for i in range( len( lowest_fitnesses ) ):
	
	print( "{" );
	print( "'x':" + str( i ) + "," );
	print( "'y':" + str( lowest_fitnesses[ i ] ) );
	print( "}," );
print( " ] }" );
print( "] };" );
print( "var fitnesses_chart = new xChart( 'line-dotted', fitnesses_data, '#fitnesses', { 'axisPaddingTop': 10, 'paddingLeft': 80 } );" );
print( "document.getElementById('probabilities').style.width  = window.innerWidth - 200 + 'px';" );
print( "document.getElementById('probabilities').style.height = window.innerHeight -300 + 'px';" );
print( "var highest_fitnesses_data = { 'xScale': 'linear', 'yScale': 'linear', 'yMax': " + str( hf_max ) +", 'yMin': " + str( hf_min ) + ", 'xMax': " + str( len( highest_fitnesses ) - 1 ) + ", 'xMin': 0, 'main': [ " );
print( "{ 'className': '.highFitnesses', 'data': [" );

for i in range( len( highest_fitnesses ) ):
	
	print( "{" );
	print( "'x':" + str( i ) + "," );
	print( "'y':" + str( highest_fitnesses[ i ] ) );
	print( "}," );
	
print( "] }" );
print( "] };" );
print( "var average_fitnesses_data = { 'xScale': 'linear', 'yScale': 'linear', 'yMax': " + str( af_max ) +", 'yMin': " + str( af_min ) + ", 'xMax': " + str( len( average_fitnesses ) - 1 ) + ", 'xMin': 0, 'main': [ " );
print( "{ 'className': '.null1', 'data': [] }," );
print( "{ 'className': '.averageFitnesses', 'data': [" );

for i in range( len( average_fitnesses ) ):
	
	print( "{" );
	print( "'x':" + str( i ) + "," );
	print( "'y':" + str( average_fitnesses[ i ] ) );
	print( "}," );
	
print( "] }" );
print( "] };" );
print( "var lowest_fitnesses_data = { 'xScale': 'linear', 'yScale': 'linear', 'yMax': " + str( lf_max ) +", 'yMin': " + str( lf_min ) + ", 'xMax': " + str( len( lowest_fitnesses ) - 1 ) + ", 'xMin': 0, 'main': [ " );
print( "{ 'className': '.null1', 'data': [] }," );
print( "{ 'className': '.null2', 'data': [] }," );
print( "{ 'className': '.lowestFitnesses', 'data': [" );

for i in range( len( lowest_fitnesses ) ):
	
	print( "{" );
	print( "'x':" + str( i ) + "," );
	print( "'y':" + str( lowest_fitnesses[ i ] ) );
	print( "}," );
	
print( "] }" );
print( "] };" );
print( "document.getElementById('highest_text').onmousedown = function ( ) { fitnesses_chart.setData( highest_fitnesses_data ); };" );
print( "document.getElementById('average_text').onmousedown = function ( ) { fitnesses_chart.setData( average_fitnesses_data ); };" );
print( "document.getElementById('lowest_text').onmousedown  = function ( ) { fitnesses_chart.setData( lowest_fitnesses_data  ); };" );
print( "document.getElementById('all_text').onmousedown  = function ( ) { fitnesses_chart.setData( fitnesses_data  ); };" );
print( " var probabilities_data = { 'xScale': 'linear', 'yScale': 'linear', 'yMax': 1.0, 'yMin': 0.0, 'xMax': " + str( len( highest_fitnesses ) - 1 ) + ", 'xMin': 0, 'main': [ " );
print( "{ 'className': '.crossoverProbabilities', 'data': [" );

for i in range( len( crossover_probabilities ) ):
	
	print( "{" );
	print( "'x':" + str( i ) + "," );
	print( "'y':" + str( crossover_probabilities[ i ] ) );
	print( "}," );
	
print( "] }," );
print( "{ 'className': '.mutationProbabilities', 'data': [" );
for i in range( len( mutation_probabilities ) ):
	
	print( "{" );
	print( "'x':" + str( i ) + "," );
	print( "'y':" + str( mutation_probabilities[ i ] ) );
	print( "}," );
print( " ] }" );
print( "] };" );
print( "var probabilities_chart = new xChart( 'line-dotted', probabilities_data, '#probabilities', { 'axisPaddingTop': 10, 'paddingLeft': 80 } );" );	
print( "var reload_timer = setTimeout( function ( ) { location.reload( true ) }, 1000 * 60 );" );
print( "</script>" );
print( "<font style='font-family: sans-serif; font-size: 10px; color: #fff;'>David Lettier (C) 2014.</font><br><br>" );
print( "</body>" );
print( "</html>" );