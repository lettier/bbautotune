#!/usr/bin/env python

import MySQLdb as mdb;
import sys;

db_connection = mdb.connect( 'localhost', '', '', 'bbautotune' );

db_cursor = db_connection.cursor( );

db_cursor.execute( "SELECT * FROM  `experimental_run` LIMIT 0, 30" );
result = db_cursor.fetchall( );

max_fitness = 0.0;

for row in result:
	
	if ( row[ 2 ] > max_fitness ):
		
		max_fitness = row[ 2 ];

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
print( "<canvas id='fitness_chart'   width='800' height='600' style='background: #fff; border: 1px #000 solid;'></canvas>" );
print( "</td>" );
print( "<td>" );
print( "<font style='font-family: sans-serif; font-size: 30px; color: rgba( 255, 10,  10, 0.8 );'>Crossover&nbsp;</font>" );
print( "<font style='font-family: sans-serif; font-size: 30px; color: #fff;'>&&nbsp;</font>" );
print( "<font style='font-family: sans-serif; font-size: 30px; color: rgba(  10, 255, 10, 0.8 );'>Mutation&nbsp;</font>" );
print( "<font style='font-family: sans-serif; font-size: 30px; color: #fff;'> Rate Progress:&nbsp;</font><br><br>" );
print( "<canvas id='cross_mut_chart' width='800' height='600' style='background: #fff; border: 1px #000 solid;'></canvas>" );
print( "</td>" );
print( "</tr>" );
print( "</table>" );
print( "<script type='text/javascript'>" );
print( "setTimeout( function ( ) { window.location.reload( false ); }, 60000 );" );
print( "var fitness_chart_context = document.getElementById( 'fitness_chart' ).getContext( '2d' );" );
print( "var fitness_data = {" );
print( "labels: [ " );

for row in result:
	
	print( "'" + str( row[ 1 ] ) + "'," );

print( "]," );
print( "datasets: [" );
print( "{" );
print( "fillColor :   'rgba( 255, 10, 10, 0.5 )'," );
print( "strokeColor : 'rgba( 255, 10, 10, 0.8 )'," );
print( "pointColor :  'rgba( 255, 10, 10, 0.8 )'," );
print( "pointStrokeColor : '#333'," );
print( "data: [" );

for row in result:
	
	print( "'" + str( row[ 2 ] ) + "'," );

print( "]" );
print( "}," );
print( "{" );
print( "fillColor :   'rgba( 10, 255, 10, 0.5 )'," );
print( "strokeColor : 'rgba( 10, 255, 10, 0.8 )'," );
print( "pointColor :  'rgba( 10, 255, 10, 0.8 )'," );
print( "pointStrokeColor : '#222'," );
print( "data: [" );

for row in result:
	
	print( "'" + str( row[ 3 ] ) + "'," );

print( "]" );
print( "}," );
print( "{" );
print( "fillColor :   'rgba( 10, 10, 200, 0.5 )'," );
print( "strokeColor : 'rgba( 10, 10, 200, 0.8 )'," );
print( "pointColor :  'rgba( 10, 10, 200, 0.8 )'," );
print( "pointStrokeColor : '#111'," );
print( "data: [" );

for row in result:
	
	print( "'" + str( row[ 4 ] ) + "'," );

print( "]" );
print( "}" );
print( "]" );
print( "};" );
print( "var fitness_chart_options = { scaleOverride: true, scaleSteps: 20.1, scaleStepWidth: " + str( max_fitness / 20 ) + ", scaleStartValue: 0.0, scaleFontFamily: \"'sans-serif'\" };" );
print( "var fitness_chart = new Chart( fitness_chart_context ).Line( fitness_data, fitness_chart_options );" );
print( "var cross_mut_chart_context = document.getElementById( 'cross_mut_chart' ).getContext( '2d' );" );
print( "var cross_mut_data = {" );
print( "labels: [ " );

for row in result:
	
	print( "'" + str( row[ 1 ] ) + "'," );

print( "]," );
print( "datasets: [" );
print( "{" );
print( "fillColor :   'rgba( 255, 10, 10, 0.5 )'," );
print( "strokeColor : 'rgba( 255, 10, 10, 0.8 )'," );
print( "pointColor :  'rgba( 255, 10, 10, 0.8 )'," );
print( "pointStrokeColor : '#333'," );
print( "data: [" );

for row in result:
	
	print( "'" + str( row[ 5 ] ) + "'," );

print( "]" );
print( "}," );
print( "{" );
print( "fillColor :   'rgba( 10, 255, 10, 0.8 )'," );
print( "strokeColor : 'rgba( 10, 255, 10, 0.8 )'," );
print( "pointColor :  'rgba( 10, 255, 10, 0.8 )'," );
print( "pointStrokeColor : '#222'," );
print( "data: [" );

for row in result:
	
	print( "'" + str( row[ 6 ] ) + "'," );

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