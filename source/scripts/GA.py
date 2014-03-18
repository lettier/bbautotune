#! /usr/bin/env python

'''

David Lettier (C) 2014.

http://www.lettier.com/

The main GA python file.

'''

import sys;
import random;
import math;
import copy;
import signal;
import time;
import itertools;
import subprocess;
import mysql.connector
import os;
import bpy;
import pickle;
import scipy;
import numpy;
import sklearn.covariance;
from bpy.props import *;

'''

Helper functions.

'''

def get_clamped_value( value, minimum, maximum ):
	
	return max( min( maximum, value ), minimum );

def get_scripts_location( ):
	
	current_working_directory = os.getcwd( );
		
	current_working_directory = current_working_directory.rsplit( "/", 1 )
	
	while ( current_working_directory[ 1 ] != "bbautotune" ):
		
		current_working_directory = current_working_directory[ 0 ].rsplit( "/", 1 );
	
	return current_working_directory[ 0 ] + "/bbautotune/source/scripts/";

'''

Creates the Blender properties for the BBAutoTune UI panel.

'''

def initialize_bbautotune_parameter_properties( ):
	
	bpy.types.Scene.GA_POPULATION_SIZE = IntProperty( 
		
		name = "Population Size",  
		description = "Population size.",
		min = 0
		
	);
	bpy.context.scene[ "GA_POPULATION_SIZE" ] = 10;
	
	bpy.types.Scene.GA_MAX_GENERATIONS = IntProperty( 
		
		name = "Max Generations", 
		description = "Max generations.",
		min = 0
		
	);
	bpy.context.scene[ "GA_MAX_GENERATIONS" ] = 100;
	
	bpy.types.Scene.GA_NUMBER_OF_ELITE = IntProperty( 
		
		name = "Number of Elite", 
		description = "Number of elite.",
		min = 0

	);
	bpy.context.scene[ "GA_NUMBER_OF_ELITE" ] = 2;

	bpy.types.Scene.GA_CROSSOVER_PROBABILITY = FloatProperty(
		
		name        = "Crossover Probability", 
		description = "Crossover probability.",
		default     = 0.8,
		min         = 0.0,
		max         = 1.0 
		
	);
	
	bpy.types.Scene.GA_MUTATION_PROBABILITY = FloatProperty(
		
		name        = "Mutation Probability", 
		description = "Mutation probability.",
		default     = 0.2,
		min         = 0.0,
		max         = 1.0 
		
	);
	
	bpy.types.Scene.GA_MAX_TORQUE = FloatProperty(
		
		name        = "Max Torque", 
		description = "Maximum torque value possible during search.",
		default     = 50.0,
		min         = 0.0,
		max         = 340282346638528859811704183484516925440.0 
		
	);
	
	bpy.types.Scene.GA_USE_RANK_SELECTION = BoolProperty( 
		
		name        = "Use Rank Selection",
		description = "Use rank selection otherwise tournament selection will be used."
		
	);	
	bpy.context.scene[ "GA_USE_RANK_SELECTION" ] = False;
	
	bpy.types.Scene.GA_PERFORM_CROSSOVER_AND_MUTATION_SEQUENTIALLY = BoolProperty( 
		
		name        = "Perform Crossover and Mutation Sequentially",
		description = "Perform crossover and mutation sequentially."
		
	);	
	bpy.context.scene[ "GA_PERFORM_CROSSOVER_AND_MUTATION_SEQUENTIALLY" ] = False;
	
	bpy.types.Scene.GA_USE_SELF_ADAPTATION = BoolProperty( 
		
		name        = "Use Self-adaptation",
		description = "Adapt the crossover and mutation probabilities."
		
	);	
	bpy.context.scene[ "GA_USE_SELF_ADAPTATION" ] = False;
	
	bpy.types.Scene.BBAUTOTUNE_OPEN_GA_MONITOR_BROWSER_WINDOW = BoolProperty( 
		
		name        = "Open GA Monitor Browser Window",
		description = "Open a browser window to the GA monitor."
		
	);	
	bpy.context.scene[ "BBAUTOTUNE_OPEN_GA_MONITOR_BROWSER_WINDOW" ] = False;
	
	bpy.types.Scene.BBAUTOTUNE_DEBUG = BoolProperty( 
		
		name        = "Debug",
		description = "Log debug information."
		
	);	
	bpy.context.scene[ "BBAUTOTUNE_DEBUG" ] = False;
 
initialize_bbautotune_parameter_properties( );

'''

The start button operator on the BBAutoTune UI panel.
Starts BBAutoTune with the values from the UI panel properties.

'''
 
class BBAUTOTUNE_UI_START_BUTTON_OPERATOR( bpy.types.Operator ):
	
	bl_idname = "bbautotune.start";
	bl_label  = "Start"

	def execute( self, context ):
	
		bpy.bbautotune.start( 
			
			bpy.context.scene.GA_POPULATION_SIZE,
			bpy.context.scene.GA_MAX_GENERATIONS,
			bpy.context.scene.GA_NUMBER_OF_ELITE,
			bpy.context.scene.GA_CROSSOVER_PROBABILITY,
			bpy.context.scene.GA_MUTATION_PROBABILITY,
			bpy.context.scene.GA_MAX_TORQUE,
			bpy.context.scene.GA_USE_RANK_SELECTION,
			bpy.context.scene.GA_PERFORM_CROSSOVER_AND_MUTATION_SEQUENTIALLY,
			bpy.context.scene.GA_USE_SELF_ADAPTATION,
			bpy.context.scene.BBAUTOTUNE_OPEN_GA_MONITOR_BROWSER_WINDOW,
			bpy.context.scene.BBAUTOTUNE_DEBUG
			
		);

		return { 'FINISHED' };

'''

The BBAutoTune UI panel and its layout in Blender.

'''

class GA_UI_PANEL( bpy.types.Panel ):
	
	bl_label       = "BBAutoTune Parameters";
	bl_space_type  = "PROPERTIES";
	bl_region_type = "WINDOW";
	bl_context     = "render";
 
	def draw( self, context ):

		self.layout.prop( context.scene, "GA_POPULATION_SIZE"                             );
		self.layout.prop( context.scene, "GA_MAX_GENERATIONS"                             );
		self.layout.prop( context.scene, "GA_NUMBER_OF_ELITE"                             );
		self.layout.prop( context.scene, "GA_CROSSOVER_PROBABILITY"                       );
		self.layout.prop( context.scene, "GA_MUTATION_PROBABILITY"                        );
		self.layout.prop( context.scene, "GA_MAX_TORQUE"                                  );
		self.layout.prop( context.scene, "GA_USE_RANK_SELECTION"                          );
		self.layout.prop( context.scene, "GA_PERFORM_CROSSOVER_AND_MUTATION_SEQUENTIALLY" );
		self.layout.prop( context.scene, "GA_USE_SELF_ADAPTATION"                         );
		self.layout.prop( context.scene, "BBAUTOTUNE_OPEN_GA_MONITOR_BROWSER_WINDOW"      );
		self.layout.prop( context.scene, "BBAUTOTUNE_DEBUG"                               );

		self.layout.operator( "bbautotune.start" );
	
'''

A single genome.

'''
	
class Genome( ):
	
	new_id = itertools.count( ).__next__;
	
	def __init__( self, genes = None, fitness = None ):
		
		self.id = Genome.new_id( );
		
		if ( not genes == None ):
			
			self.genes = list( genes );
			
		else:
			
			self.genes = [ ];
		
		self.fitness = fitness or 0.0;
		
		# Used to calculate either the crossover progress or mutation progress.
		# If this genome is created via crossover, use the weighted average
		# based on the cross over point.
		# So if the crossover point is say 9 and the genome length is 10,
		# then the weighted average pf = (p1.f*.9) + (p2.f*.1).
		# In other words the offspring received 90% of its genes from parent one
		# and it received 10% of its genes from parent two so its parent fitness is
		# 90% of parent one's fitness and 10% of parent two's fitness.
		
		self.parent_fitness = 0.0;
		
		# Created by means if this genome was generated either by randomness, crossover, 
		# mutation, both crossover and mutation, or elitism.
		# Initially it is created from nothing so set it to -1.
		# 0 = randomness, 1 = crossover, 2 = mutation, 3 = crossover & mutation, 4 = elitism

		# This encoding is to facilitate crossover's and mutation's progress at producing fitter
		# offspring than the offspring's parents.
		
		self.created_by = 0;
		
	def set_genes( self, genes = None ):
		
		if ( not genes == None ):
			
			self.genes = list( genes );
			
		else:
			
			self.genes = [ ];
			
	def get_genes( self ):
		
		return list( self.genes );
	
	def get_genes_as_string( self ):
		
		return ",".join( map( str, self.genes ) );
		
	def set_fitness( self, fitness = None ):
		
		self.fitness = fitness or 0.0;
			
	def get_fitness( self ):
		
		return self.fitness;
	
	def set_parent_fitness( self, parent_fitness = None ):
		
		self.parent_fitness = parent_fitness or 0.0;
			
	def get_parent_fitness( self ):
		
		return self.parent_fitness;
	
	def set_created_by( self, created_by = None ):
		
		self.created_by = created_by or 0;
			
	def get_created_by( self ):
		
		return self.created_by;
	
	def __repr__( self ):
		
		return repr( ( self.id, self.created_by, self.fitness, self.parent_fitness, self.genes ) );
	
'''

The main genetic algorithm object.

'''
 
class Genetic_Algorithm( ):
	
	def __init__( 
		
		self,
		population_size                             = None,
		max_generations                             = None,
		number_of_elite                             = None,
		crossover_probability                       = None,
		mutation_probability                        = None,
		use_rank_selection                          = None,
		perform_crossover_and_mutation_sequentially = None,
		use_self_adaptation                         = None
		
	):
		
		'''
		
		Begin parameters.
		
		'''
		
		# Size of population.
		
		self.population_size = population_size or 0;
		
		# Number of generations to run until termination of the algorithm.
		
		self.max_generations = max_generations or 0;
		
		# Set the number of elite that go on to the next generation.
		
		self.number_of_elite = number_of_elite or 0;
		
		# Probability of genome's crossing over bits.
		# 0.7 is pretty good.
		
		self.crossover_probability               = crossover_probability or 0.0;
		self.crossover_probability_minimum       = 0.001;
		self.crossover_probability_adjustment    = 0.01;
		self.crossover_operator_progress_average = 0.0;
		self.observed_crossover_rate             = 0.0;	
		self.total_number_of_crossovers          = 0;
		self.total_number_of_crossover_attempts  = 0;
		
		# Probability that a genomes bits will mutate.
		# Try figures around 0.05 to 0.3-ish.

		self.mutation_probability               = mutation_probability or 0.0;
		self.mutation_probability_minimum       = 0.001;
		self.mutation_probability_adjustment    = 0.01;
		self.mutation_operator_progress_average = 0.0;
		self.observed_mutation_rate             = 0.0;
		self.total_number_of_mutations          = 0;
		self.total_number_of_mutation_attempts  = 0;
		
		# Use rank selection?
		
		self.use_rank_selection = use_rank_selection or False;
		
		# Perform crossover and mutation sequentially or separately?
		
		self.perform_crossover_and_mutation_sequentially = perform_crossover_and_mutation_sequentially or False;
		
		# Use self-adaptation?
		
		self.use_self_adaptation = use_self_adaptation or False;
		
		'''
		
		End parameters.
		
		'''
		
		# Log file if debugging.
		
		self.log_file_name = "";
		
		# The amount of genes per genome.
		
		self.number_of_genes_per_genome = 18;
		
		# This holds the entire population of genomes.
		
		self.population = [ ];

		# Total fitness of population.
		
		self.total_fitness = 0.0;	

		# Average fitness.
		
		self.average_fitness = 0.0;
		
		# Highest fitness.
		
		self.highest_fitness = 0.0;

		# Lowest fitness.
		
		self.lowest_fitness = 0.0;

		# Keeps track of the best genome.
		
		self.fittest_genome_index = -1;

		# Keep track of the worst genome.
		
		self.weakest_genome_index = -1;

		# Generation number.
		
		self.generation_number = 0;

		# Current population makeup of randoms, crossovers, mutants, crossover mutants, and elites.

		self.population_makeup = "";
		
	def set_population_size( self, size = None ):
		
		self.population_size = size or 0;
		
	def get_population_size( self ):
		
		return self.population_size;
	
	def set_max_generations( self, maximum = None ):
		
		self.max_generations = maximum or 0;
		
	def get_max_generations( self ):
		
		return self.max_generations;
		
	def set_crossover_probability( self, probability = None ):
		
		self.crossover_probability = probability or 0;
		
	def get_crossover_probability( self ):
		
		return self.crossover_probability;
	
	def set_mutation_probability( self, probability = None ):
		
		self.mutation_probability = probability or 0;
		
	def get_mutation_probability( self ):
		
		return self.mutation_probability;
	
	def set_number_of_genes_per_genome( self, number_of = None ):
		
		self.number_of_genes_per_genome = number_of or 0;
		
	def get_number_of_genes_per_genome( self ):
		
		return self.number_of_genes_per_genome;
	
	def set_use_rank_selection( self, boolean = None ):
		
		self.use_rank_selection = boolean or 0;
		
	def get_use_rank_selection( self ):
		
		return self.use_rank_selection;
	
	def set_perform_crossover_and_mutation_sequentially( self, boolean = None ):
		
		self.perform_crossover_and_mutation_sequentially = boolean or 0;
		
	def get_perform_crossover_and_mutation_sequentially( self ):
		
		return self.perform_crossover_and_mutation_sequentially;
	
	def set_use_self_adaptation( self, use_self_adaptation = None ):
		
		self.use_self_adaptation = use_self_adaptation or False;
		
	def get_use_self_adaptation( self ):
		
		return self.use_self_adaptation;
	
	def set_number_of_elite( self, number_of = None ):
		
		self.number_of_elite = number_of or 0;
		
		if ( self.number_of_elite > self.population_size ):
			
			self.number_of_elite = self.population_size;
		
	def get_number_of_elite( self ):
		
		return self.number_of_elite;
	
	def set_log_file_name( self, log_file_name ):
		
		self.log_file_name = log_file_name;
		
	def get_log_file_name( self ):
		
		return self.log_file_name;
	
	def log( self, log_string ):
		
		if ( self.log_file_name != "" ):
			
			log_file = open( self.log_file_name, "a+" );
			
			log_file.write( log_string + "\n" );
			
			log_file.close( );
	
	def set_total_fitness( self, total_fitness = None ):
		
		self.total_fitness = total_fitness or 0;
		
	def get_total_fitness( self ):
		
		return self.total_fitness;
	
	def set_average_fitness( self, average_fitness = None ):
		
		self.average_fitness = average_fitness or 0;
		
	def get_average_fitness( self ):
		
		return self.average_fitness;
	
	def set_highest_fitness( self, highest_fitness = None ):
		
		self.highest_fitness = highest_fitness or 0;
		
	def get_highest_fitness( self ):
		
		return self.highest_fitness;
	
	def set_lowest_fitness( self, lowest_fitness = None ):
		
		self.lowest_fitness = lowest_fitness or 0;
		
	def get_lowest_fitness( self ):
		
		return self.lowest_fitness;
	
	def set_fittest_genome_index( self, fittest_genome_index = None ):
		
		self.fittest_genome_index = fittest_genome_index or -1;
		
	def get_fittest_genome_index( self ):
		
		return self.fittest_genome_index;
	
	def set_weakest_genome_index( self, weakest_genome_index = None ):
		
		self.weakest_genome_index = weakest_genome_index or -1;
		
	def get_fittest_genome_index( self ):
		
		return self.weakest_genome_index;
	
	def set_generation_number( self, generation_number = None ):
		
		self.generation_number = generation_number or 0;
		
	def get_generation_number( self ):
		
		return self.generation_number;
	
	def get_population_makeup( self ):
	
		self.compute_population_makeup( );
		
		return self.population_makeup;
	
	def get_genome( self, index ):
		
		assert index < self.population_size and index >= 0, "Genome index out of bounds.";
		
		return copy.deepcopy( self.population[ index ] );
	
	def get_genome_fitness( self, index ):
		
		assert index < self.population_size and index >= 0, "Genome index out of bounds.";
		
		return self.population[ index ].fitness;
	
	def set_genome_fitness( self, index, fitness ):
		
		assert index < self.population_size and index >= 0, "Genome index out of bounds.";
		
		self.population[ index ].set_fitness( fitness ); 
	
	def get_genome_genes_as_string( self, index ):
		
		assert index < self.population_size and index >= 0, "Genome index out of bounds.";
		
		return self.population[ i ].get_genes_as_string( );
	
	def get_population_genes_as_string( self ):
		
		if ( self.population_size == 0 ):
			
			return "";
		
		else:
		
			gene_string = self.population[ 0 ].get_genes_as_string( );
		
			for i in range( self.population_size ):
				
				gene_string += "," + self.population[ i ].get_genes_as_string( );
				
			return gene_string;
		
	def create_randomized_population( self ):
		
		self.log( "Generating random population." );
		
		self.population = [ ];
		
		# Initialize population with genomes consisting of random
		# genes and all fitness's set to zero.
		
		for i in range( self.population_size ):

			self.population.append( Genome( ) );
			
			self.log( "Genome: " + str( i ) );

			for j in range( self.number_of_genes_per_genome ):
				
				random_gene = random.uniform( 0.0, 1.0 );
				
				self.log( "Random gene: " + str( j ) );
				
				self.log( str( random_gene ) );
				
				self.population[ i ].genes.append( random_gene );
				
		self.set_generation_number( 0 );
		
		self.update_population_metrics( );
	
	def replace_population_genes( self, replacement_population_genes ):
		
		# Assumes replacement_population_genes is one big array. 
		# Splices the big array based on the number of genes per genome.
		
		# Big array:  [ 1,2,3,4,5,6,7,8,9,10 ]
		# Number of genes per genome: 2
		# Population: [ [ 1,  2 ] G0
		#               [ 3,  4 ] G1
		#               [ 5,  6 ] ...
		#               [ 7,  8 ] ...
		#               [ 9, 10 ] GN-1
		#             ]
		
		assert len( replacement_population_genes ) != 0, "Replacement gene size is zero.";
		
		assert len( replacement_population_genes ) == self.population_size * self.number_of_genes_per_genome, "Too few or too many replacement genes."
		
		k = 0;
		
		for i in range( self.population_size ):

			self.population[ i ].genes = [ ];
			
			for j in range( self.number_of_genes_per_genome ):

				self.population[ i ].genes.append( replacement_population_genes[ k ] );
				
				k += 1;
				
	def selection_operator( self, number_of_indexes ):
		
		self.log( "Entering selection operator." );
		
		self.log( str( number_of_indexes ) + " genomes requested." );

		# Assumes the population has been evaluated.
		
		# Assumes the population is sorted in descending order according to fitness.
		
		if ( not self.use_rank_selection ):
			
			tournament_size = number_of_indexes + 1;
			
			assert tournament_size <= self.population_size and tournament_size >= 0, "Tournament size too large/small.";
			
			genome_indexes_selected = [ ];
			
			self.log( "Selecting random players." );
			
			for i in range( number_of_indexes ):
				
				tournament_players = [ ];
			
				for j in range( tournament_size ):
					
					random_int = random.randint( 0, self.population_size - 1 );
					
					tournament_players.append( [ random_int, self.population[ random_int ].get_fitness( ) ] );
					
					self.log( "Random players selected." );
						
					self.log( str( tournament_players ) );
					
				# Remember, lower fitness values are a higher fitness.
				# Sorts list in ascending orderer.
				# tournament_players = [ [genome_index,genome_fitness], ... ]
				# [ 0 ][ 0 ] = get the index with the lowest fitness value (thus the highest fitness ).
					
				player_ranking = sorted( tournament_players, key = lambda x: x[ 1 ] );
				
				self.log( "Player ranking." );
				
				self.log( str( player_ranking ) );
				
				winner = player_ranking[ 0 ][ 0 ];
				
				self.log( "Winner." );
				
				self.log( str( winner ) );
				
				genome_indexes_selected.append( winner );
						
			self.log( "Selected genomes with tournament selection." );
			
			self.log( str( genome_indexes_selected ) );
			
			return genome_indexes_selected;
		
		else:
		
			self.log( "Sorted?" );
			
			self.log( str( self.population[ 0 ].get_fitness( ) ) + " " + str( self.population[ -1 ].get_fitness( ) ) );
			
			# Assume the genomes are sorted in non-increasing order of fitness.
			
			# Give the worst genome a rank fitness of 1.
			# Give the second worst genome a rank fitness of 2.
			# ...
			# Give the best genome a rank fitness of the population size.
			
			genome_indexes_selected = [ ];

			# Genomes:               1, 2, 3,  4
			# Genomes fitnesses:     4, 2, 3,  1 (Lowest is highest. )
			# Rank fitnesses:        1, 2, 3,  4 (Highest is highest.)
			# Partial sums:          1, 3, 6, 10
			# Random number U(0,10): 7
			# Genome 4 is selected.
			# Since all random numbers are uniform,
			# Genome 1 has a probability of being selected:  (1-0)*(1/10) =  10%
			# Genome 2 has a probability of being selected:  (3-1)*(1/10) =  20%
			# Genome 3 has a probability of being selected:  (6-3)*(1/10) =  30%
			# Genome 4 has a probability of being selected: (10-6)*(1/10) =  40%
			# Total of any being selected:                                = 100%
			#    |
			#    
			# 0.10 ---------------------------------------
			#     |   |       |           |               |
			#     |   |       |           |               |
			#     0---1---2---3---4---5---6---7---8---9---10
			#         G1      G2          G3              G4
						
			# Individual rank fitnesses.
			
			rank_fitnesses = [ ];
			
			for i in range( self.population_size ):
				
				rank_fitnesses.append( i + 1 );
				
			total_rank_fitness = sum( rank_fitnesses );
			
			self.log( "Total rank fitness." );
			
			self.log( str( total_rank_fitness ) );
			
			# Partial sum. P[i] = sum( P[1:i] ) where i is in range [1,n].
			
			partial_sums = list( itertools.accumulate( rank_fitnesses ) );
				
			self.log( "Partial sums." );
			
			self.log( str( partial_sums ) );
			
			while ( len( genome_indexes_selected ) < number_of_indexes ):
				
				random_number = random.randint( 0, total_rank_fitness );
				
				self.log( "Random number: " + str( random_number ) );
				
				for i in range( self.population_size ):
					
					if ( partial_sums[ i ] >= random_number ):
						
						self.log( "Partial sum: " + str( partial_sums[ i ] ) );
	       
						self.log( "Genome index selected: " + str( i ) );
						
						genome_indexes_selected.append( i );
						
						break;
						
					if ( len( genome_indexes_selected ) == number_of_indexes ):
						
						break;
						
			self.log( "Selected genomes with rank selection." );
			
			self.log( str( genome_indexes_selected ) );
			
			return genome_indexes_selected;
	
	def elitism_operator( self, new_population ):
		
		self.log( "Attempting to add elite genomes." );

		if ( self.number_of_elite > self.population_size ):
			
			self.number_of_elite = self.population_size;
		
		# Assumes the population is sorted in ascending order of fitness.
		
		# A = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
		# |A| = 10
		# i = 2 check.
		# i = 1 decrement.
		# A[ ( ( 10 - 1 = 9 ) - i ) = 8 ]
		# i = 1 check.
		# i = 0 decrement.
		# A[ ( ( 10 - 1 = 9 ) - i ) = 9 ]
		# i = 0 check.
		# Stop.
		
		i = self.number_of_elite;
		
		while ( i ):
			
			i -= 1;

			genome_temp = copy.deepcopy( self.population[ ( self.population_size - 1 ) - i ] );
			
			self.log( "Adding elite genome. Its fitness: " + str( genome_temp.get_fitness( ) ) );
			
			genome_temp.fitness        = 0.0;
			genome_temp.parent_fitness = 0.0;
			genome_temp.created_by     = 4;	
			
			new_population.append( genome_temp );
			
			if ( len( new_population ) == self.population_size ):
				
				break;
				
	def crossover_operator( self, parent_one_index, parent_two_index ):

		# One point crossover operator.
		
		# Do we crossover?
		
		self.log( "Attempting crossover." );
		
		if ( random.uniform( 0.0, 1.0 ) <= self.crossover_probability ):
		
			# If the parents are the same genome then this is not a true crossover.
			
			if ( parent_one_index == parent_two_index ):
				
				self.log( "Parents are the same. Crossover failed." );
				
				return 0;
			
			self.log( "Parent indexes." );
				
			self.log( str( parent_one_index ) + " " + str( parent_two_index ) );
			
			# Only returns one crossed offspring.
			
			offspring = Genome( );

			# Determine a crossover point.
			
			# Let the uniform sample be in the range of [1,n-1].
			# If the crossover point was zero than no true crossover takes place
			# as all of one parent's genes get copied into the offspring.
			# If the cp = n-1 then at least you get n-1 from one parent and 1
			# from another parent.
			
			crossover_point = random.randint( 1, ( self.number_of_genes_per_genome - 1 ) );
			
			self.log( "Crossover point." );
			
			self.log( str( crossover_point ) );

			# Cross the parent's genes in the offspring.
			
			offspring.genes = [ ];
			
			offspring.fitness = 0.0;
			
			offspring.parent_fitness = 0.0;
			
			for i in range( crossover_point ):
				
				offspring.genes.append( copy.deepcopy( self.population[ parent_one_index ].genes[ i ] ) );

			for i in range( crossover_point, self.number_of_genes_per_genome ):

				offspring.genes.append( copy.deepcopy( self.population[ parent_two_index ].genes[ i ] ) );
			
			# Determine if a crossover actually took place.
			# The offspring should not match the parent one's genes and
			# it should not match parent two's genes as the offspring
			# should be a combination of the two.
			
			if (    ( offspring.genes != self.population[ parent_one_index ].genes ) and
				( offspring.genes != self.population[ parent_two_index ].genes )     ):
					
				# Weighted average fitness of the parents based on crossover point
				# determining percentage of genes received from parent one and parent two.
				# Let the number of genes per genome be 41 and let the crossover point be 1. 
				# Offspring gets [0,1) = 1 gene from parent one and [1,41) = 40 genes from parent two. 
				# PF = PF1 * (1/41) + PF2 * ((41-1)/41).
				
				parent_one_contribution = ( self.population[ parent_one_index ].fitness * ( (                                   crossover_point ) / ( self.number_of_genes_per_genome ) ) );
				parent_two_contribution = ( self.population[ parent_two_index ].fitness * ( ( self.number_of_genes_per_genome - crossover_point ) / ( self.number_of_genes_per_genome ) ) );
				
				offspring.parent_fitness = parent_one_contribution + parent_two_contribution;
				
				self.log( "Parent fitness contributions." );
				
				self.log( str( parent_one_contribution ) );
				
				self.log( str( parent_two_contribution ) );
				
				offspring.created_by = 1;
				
				self.log( "Returning crossed offspring." );
				
				return offspring;
	
			else:
				
				self.log( "Did not actually perform crossover." );

				return 0;
			
		else:
			
			self.log( "Greater than crossover probability." ); 
			
			return 0;
		
	def mutation_operator( self, parent_index ):

		# Mutates parent genome's genes on a whole genome basis based on the mutation probability.
		
		# Gaussian distribution mutation. 
		
		# Do we mutate?
		
		self.log( "Attempting mutation." );
		
		if ( random.uniform( 0.0, 1.0 ) <= self.mutation_probability ):
			
			# Create a new offspring.
			
			offspring                = Genome( );
			offspring.genes          = [ ];
			offspring.genes          = copy.deepcopy( self.population[ parent_index ].genes );
			offspring.fitness        = 0.0;
			offspring.parent_fitness = 0.0;
			
			# Begin to mutate.
			
			mutated = False;
			
			for i in range( self.number_of_genes_per_genome ):

				# Mutate this gene by sampling a value from a normal distribution
				# where the mean is the current gene value and the standard deviation
				# is the mutation step equal to the mutation probability in the range [0,1].
				# A low mutation probability will give a mutated gene value closer to the original gene 
				# value (the mean) (most of the time) as the standard deviation is small and therefore the mutation step is small. 
				# A high mutation probability will give a mutated gene value farther from the original gene 
				# value (the mean) as the standard deviation is large and therefore the mutation step is large. 
				
				# Note that gv = gv + σ*N(0,1) is the same as gv = N(gv,σ).

				# Clamp the gene to range [-1,1].
				
				temp_gene_value = copy.deepcopy( offspring.genes[ i ] );
				
				offspring.genes[ i ] = random.gauss( offspring.genes[ i ], self.mutation_probability );
				offspring.genes[ i ] = get_clamped_value( offspring.genes[ i ], 0.0, 1.0 );
				
				self.log( "Mutation value before/after." );
				
				self.log( str( temp_gene_value ) + " " + str( offspring.genes[ i ] ) );
				
				# Test if it was truly mutated.
				
				if ( temp_gene_value != offspring.genes[ i ] ):

					mutated = True;
			
			if ( mutated ): # If truly mutated.

				offspring.parent_fitness = self.population[ parent_index ].fitness;
			
				offspring.created_by = 2;		
				
				return offspring;

			else:
				
				self.log( "Mutation did not actually take place." );

				return 0;

		else:
			
			self.log( "Greater than mutation probability." );
			
			return 0;
		
	def crossover_then_mutate_operator( self, parent_one_index, parent_two_index ):

		# Crossover and mutation done sequentially as in more traditional genetic algorithms.
		
		# First attempts crossover and then attempts mutation.
		
		self.log( "Attempting crossover and then mutation." );
		
		offspring_one = copy.deepcopy( self.population[ parent_one_index ] );
		offspring_two = copy.deepcopy( self.population[ parent_one_index ] );
		
		offspring_one.fitness = 0.0;
		offspring_two.fitness = 0.0;
		
		offspring_one.parent_fitness = 0.0;
		offspring_two.parent_fitness = 0.0;
		
		offspring_one.created_by = 0;
		offspring_two.created_by = 0;
		
		self.log( "Attempting crossover first." );
		
		# Attempt crossover.

		crossover_point = random.randint( 0, ( self.number_of_genes_per_genome - 1 ) );
		
		self.log( "Crossover point." );
			
		self.log( str( crossover_point ) );
		
		if ( ( random.uniform( 0.0, 1.0 ) <= self.crossover_probability ) and ( parent_one_index != parent_two_index ) and ( crossover_point != 0 ) ):

			# Cross the parent's genes in the offspring.

			offspring_one.genes = [ ];
			offspring_two.genes = [ ];
			
			for i in range( crossover_point ):
				
				offspring_one.genes.append( copy.deepcopy( self.population[ parent_one_index ].genes[ i ] ) );
				offspring_two.genes.append( copy.deepcopy( self.population[ parent_two_index ].genes[ i ] ) );

			for i in range( crossover_point, self.number_of_genes_per_genome ):
				
				offspring_one.genes.append( copy.deepcopy( self.population[ parent_two_index ].genes[ i ] ) );
				offspring_two.genes.append( copy.deepcopy( self.population[ parent_one_index ].genes[ i ] ) );

			parent_one_contribution = ( self.population[ parent_one_index ].fitness * ( (                                   crossover_point ) / ( self.number_of_genes_per_genome ) ) );
			parent_two_contribution = ( self.population[ parent_two_index ].fitness * ( ( self.number_of_genes_per_genome - crossover_point ) / ( self.number_of_genes_per_genome ) ) );	
			
			offspring_one.parent_fitness = parent_one_contribution + parent_two_contribution;
			offspring_one.created_by     = offspring_one.created_by + 1;

			parent_two_contribution = ( self.population[ parent_two_index ].fitness * ( (                                   crossover_point ) / ( self.number_of_genes_per_genome ) ) );
			parent_one_contribution = ( self.population[ parent_one_index ].fitness * ( ( self.number_of_genes_per_genome - crossover_point ) / ( self.number_of_genes_per_genome ) ) );	
			
			offspring_two.parent_fitness = parent_two_contribution  + parent_one_contribution;
			offspring_two.created_by     = offspring_two.created_by + 1;
			
		else:
			
			self.log( "Crossover failed." );

		# Crossover may or may not have happened but now try mutation.
		
		self.log( "Attempting mutation second." );

		# Attempt to mutate offspring one.
		
		self.log( "Attempting to mutate the first offspring." );
		
		mutated_one = False;
		
		for i in range( self.number_of_genes_per_genome ):

			# Mutate this gene by sampling a value from a normal distribution where the mean
			# is the current gene value and the standard deviation is mutation step equal to the 
			# mutation probability in the range [0,1]. A low mutation probability will give a mutated gene 
			# value close to the original gene value (the mean) (most of the time) as the standard 
			# deviation is small and therefore the mutation step is small. A high mutation probability
			# will give, or it can more easily, mutate a gene value farther from the original gene value 
			# (the mean) as the standard deviation is large and therefore the mutation step is large. 
			
			# Note that gv = gv + σ * N( 0, 1 ) is the same as gv = N( gv, σ ).

			# Clamp the gene to range [0,1].
			
			if ( random.uniform( 0.0, 1.0 ) <= self.mutation_probability ): # Mutate this gene?
			
				temp_gene_value_one = copy.deepcopy( offspring_one.genes[ i ] );
				
				offspring_one.genes[ i ] = random.gauss( offspring_one.genes[ i ], self.mutation_probability );
				# offspring_one.genes[ i ] = gaussian_distribution( offspring_one.genes[ i ], 0.5 );
				# offspring_one.genes[ i ] = offspring_one.genes[ i ] + ( get_random_float( -1.0, 1.0 ) * .3 );
				
				offspring_one.genes[ i ] = get_clamped_value( offspring_one.genes[ i ], 0.0, 1.0 );
				
				self.log( "Mutation value before/after." );
				
				self.log( str( temp_gene_value_one ) + " " + str( offspring_one.genes[ i ] ) );
				
				# Test if it was truly mutated.
				
				if ( temp_gene_value_one != offspring_one.genes[ i ] ):
				
					mutated_one = True;
	
		# Attempt to mutate offspring two.
		
		self.log( "Attempting to mutate the second offspring." );
		
		mutated_two = False;
		
		for i in range( self.number_of_genes_per_genome ):

			# Mutate this gene by sampling a value from a normal distribution where the mean
			# is the current gene value and the standard deviation is mutation step equal to the 
			# mutation probability in the range [0,1]. A low mutation probability will give a mutated gene 
			# value close to the original gene value (the mean) (most of the time) as the standard 
			# deviation is small and therefore the mutation step is small. A high mutation probability
			# will give (or it can more easily) mutate a gene value farther from the original gene value 
			# (the mean) as the standard deviation is large and therefore the mutation step is large. 
			
			# Note that gv = gv + σ * N( 0, 1 ) is the same as gv = N( gv, σ ).

			# Clamp the gene to range [0,1].
			
			if ( random.uniform( 0.0, 1.0 ) <= self.mutation_probability ): # Mutate this gene?
				
				temp_gene_value_two = copy.deepcopy( offspring_two.genes[ i ] );
				
				offspring_two.genes[ i ] = random.gauss( offspring_two.genes[ i ], self.mutation_probability );
				# offspring_two.genes[ i ] = gaussian_distribution( offspring_two.genes[ i ], 0.5 );
				# offspring_two.genes[ i ] = offspring_two.genes[ i ] + ( get_random_float( -1.0, 1.0 ) * .3 );
				
				offspring_two.genes[ i ] = get_clamped_value( offspring_two.genes[ i ], 0.0, 1.0 );
				
				self.log( "Mutation value before/after." );
				
				self.log( str( temp_gene_value_two ) + " " + str( offspring_one.genes[ i ] ) );
				
				# Test if it was truly mutated.
				
				if ( temp_gene_value_two != offspring_two.genes[ i ] ):
				
					mutated_two = True;
		
		if ( mutated_one ): # If truly mutated.
		
			# Mutation = 2, crossover = 1, crossover + mutation = 3.
			
			offspring_one.created_by = offspring_one.created_by + 2;
			
			# If this offspring was only mutated, that is, it was not crossed then get its parent fitness.
			# It it was crossed before being mutated then offspring_one.created would equal 3.
			
			if ( offspring_one.created_by == 2 ):
				
				self.log( "Offspring one only mutated." );
			
				offspring_one.parent_fitness = copy.deepcopy( self.population[ parent_one_index ].fitness );
		
		if ( mutated_two ): # If truly mutated.
		
			offspring_two.created_by = offspring_two.created_by + 2;

			# If this offspring was only mutated, that is, it was not crossed then get its parent fitness.
			# It it was crossed before being mutated then offspring_two.created would equal 3.
			
			if ( offspring_two.created_by == 2 ):
				
				self.log( "Offspring two only mutated." );
			
				offspring_two.parent_fitness = copy.deepcopy( self.population[ parent_two_index ].fitness );
		
		# No parents->offspring not crossed and/or not mutated enter into the new population.
		# Each offspring going into the new population must either crossed, mutated, or both.
		
		if ( ( offspring_one.created_by == 0 ) or ( offspring_two.created_by == 0 ) ):
			
			self.log( "No crossover and/or mutation occured." );
			
			return 0;
		
		elif ( ( offspring_one.genes == self.population[ parent_one_index ].genes ) or ( offspring_two.genes == self.population[ parent_two_index ].genes ) ):

			self.log( "Offspring genes not different from parents." );

			return 0;

		else:
			
			self.log( "Returning offspring." );

			return { "one": offspring_one, "two": offspring_two };
		
	def reset_population_metrics( self ):

		self.total_fitness         =  0.0;
		self.highest_fitness       =  0.0;
		self.lowest_fitness        =  0.0;
		self.average_fitness       =  0.0;
		self.fittest_genome_index  = -1;
		self.weakest_genome_index  = -1;
		
	def update_population_metrics( self ):
		
		# 0.0 is the highest fitness
		# 1.7976931348623157e+308 is lowest fitness.

		self.reset_population_metrics( );

		highest_so_far = self.population[ 0 ].fitness;
		lowest_so_far  = self.population[ 0 ].fitness;
		
		self.fittest_genome_index = 0;
		self.weakest_genome_index = 0;
		
		self.total_fitness   = self.population[ 0 ].fitness;
		self.highest_fitness = self.population[ 0 ].fitness;
		self.lowest_fitness  = self.population[ 0 ].fitness;

		for i in range( self.population_size ):
			
			# Update fittest if necessary.
			
			if ( highest_so_far > self.population[ i ].fitness ):

				highest_so_far = self.population[ i ].fitness;

				self.fittest_genome_index = i;

				self.highest_fitness = highest_so_far;

			# Update worst if necessary.
			
			if ( lowest_so_far < self.population[ i ].fitness ):

				lowest_so_far = self.population[ i ].fitness;
				
				self.weakest_genome_index = i;

				self.lowest_fitness = lowest_so_far;

			self.total_fitness += self.population[ i ].fitness;
			
			# Next genome.

		self.average_fitness = self.total_fitness / float( self.population_size );
		
		self.log( "Population metrics. T H L A Fi Wi." );
		
		self.log( str( self.total_fitness        ) );
		self.log( str( self.highest_fitness      ) );
		self.log( str( self.lowest_fitness       ) );
		self.log( str( self.average_fitness      ) );
		self.log( str( self.fittest_genome_index ) );
		self.log( str( self.weakest_genome_index ) );
		
	def compute_population_makeup( self ):
		
		randoms           = 0;
		crossovers        = 0;
		mutants           = 0;
		crossover_mutants = 0;
		elites            = 0;

		for i in range( self.population_size ):

			if ( self.population[ i ].created_by == 0 ):

				randoms = randoms + 1;

			elif ( self.population[ i ].created_by == 1 ):

				crossovers = crossovers + 1;

			elif ( self.population[ i ].created_by == 2 ):

				mutants = mutants + 1;

			elif ( self.population[ i ].created_by == 3 ):

				crossover_mutants = crossover_mutants + 1;

			elif ( self.population[ i ].created_by == 4 ):

				elites = elites + 1;

		self.population_makeup = str( randoms ) + " " + str( crossovers ) + " " + str( mutants ) + " " + str( crossover_mutants ) + " " + str( elites );

		self.log( "Population makeup. R C M CM E." );
		
		self.log( self.population_makeup );

	def adapt_crossover_and_mutation_probabilities( self ): 
		
		# Calculate the crossover and mutation operators' progress where 
		# their progress is based on how well they produced offspring that
		# had a better fitness than their parent.
		
		self.log( "Adapting crossover and mutation probabilities." );
		
		crossover_operator_progress_sum = 0.0;
		number_of_crossovers            = 0;
		
		mutation_operator_progress_sum  = 0.0;
		number_of_mutations             = 0;
		
		# Sum all of the progresses.
		
		# Since the GA is looking to minimize the fitness function, progress is when the offspring has a lower fitness score
		# than its parent.
		
		for i in range( self.population_size ):

			if ( self.population[ i ].created_by == 1 ): # Created by crossover.

				crossover_operator_progress_sum += ( self.population[ i ].parent_fitness - self.population[ i ].fitness );
				
				number_of_crossovers += 1;
			
			elif ( self.population[ i ].created_by == 2 ): # Created by mutation.

				mutation_operator_progress_sum  += ( self.population[ i ].parent_fitness - self.population[ i ].fitness );
				
				number_of_mutations += 1;
				
		# Now calculate the average crossover and mutation progress for the population.
		
		self.crossover_operator_progress_average = 0.0;
		self.mutation_operator_progress_average  = 0.0;
		
		if ( number_of_crossovers != 0 ):

			self.crossover_operator_progress_average = ( crossover_operator_progress_sum ) / float( number_of_crossovers );			

		if ( number_of_mutations != 0 ):

			self.mutation_operator_progress_average  = ( mutation_operator_progress_sum ) / float( number_of_mutations );			

		# Adjust crossover and mutation rate adjustments.
		
		self.log( "Adjusting crossover and mutation rate adjustments." );
		
		if ( self.lowest_fitness > self.highest_fitness ):
			
			self.log( "L > H" );

			self.crossover_probability_adjustment = 0.01 * ( ( self.lowest_fitness - self.average_fitness ) / ( self.lowest_fitness - self.highest_fitness ) );
			
			self.mutation_probability_adjustment  = 0.01 * ( ( self.lowest_fitness - self.average_fitness ) / ( self.lowest_fitness - self.highest_fitness ) );

			self.log( str( self.crossover_probability_adjustment ) + " " + str( self.mutation_probability_adjustment ) );

		elif ( self.lowest_fitness == self.average_fitness ):
			
			self.log( "L == A" );

			self.crossover_probability_adjustment = 0.01;
			
			self.mutation_probability_adjustment  = 0.01;
			
		self.log( "Crossover progress average." );
			
		self.log( str( self.crossover_operator_progress_average ) );
		
		self.log( "Mutation progress average." );
			
		self.log( str( self.mutation_operator_progress_average ) );

		# Adjust crossover and mutation rates.
		
		if ( self.crossover_operator_progress_average > self.mutation_operator_progress_average ):
			
			self.log( "Adjusting crossover/mutation probabilities. CPA > MPA." );

			self.crossover_probability = self.crossover_probability + self.crossover_probability_adjustment;
			
			self.mutation_probability  = self.mutation_probability  - self.mutation_probability_adjustment;

		elif ( self.crossover_operator_progress_average < self.mutation_operator_progress_average ):
			
			self.log( "Adjusting crossover/mutation probabilities. CPA < MPA." );

			self.crossover_probability = self.crossover_probability - self.crossover_probability_adjustment;
			
			self.mutation_probability  = self.mutation_probability  + self.mutation_probability_adjustment;

		elif ( self.crossover_operator_progress_average == self.mutation_operator_progress_average ):
			
			self.log( "Not adjusting crossover/mutation probabilities. CPA == MPA." );

			# Do not adjust.
			
			pass;
		
		self.crossover_probability = get_clamped_value( self.crossover_probability, self.crossover_probability_minimum, 1.0 - self.mutation_probability_minimum  );
		
		self.mutation_probability  = get_clamped_value( self.mutation_probability,  self.mutation_probability_minimum,  1.0 - self.crossover_probability_minimum );		
		
	def sort_population( self, descending = None ):
		
		self.log( "Sorting population. Descending: " + str( descending ) );

		if ( descending == None or descending == False ):

			self.population = sorted( self.population, key = lambda genome: genome.fitness, reverse = False );

		elif ( descending == True ):

			self.population = sorted( self.population, key = lambda genome: genome.fitness, reverse = True );
			
		self.log( "Sorted." );
			
		self.log( str( self.population[ 0 ].fitness ) + " " + str( self.population[ -1 ].fitness ) );
			
	def generate_new_generation( self ):
		
		self.log( "Creating a new generation." );

		# Sort the population based on fitness in ascending order.
		# 0.0 is the highest fitness and infinity is the lowest fitness.
		# So sort in non-increasing order.
		
		self.log( "Sorting population." );
		
		self.sort_population( descending = True );
		
		# Update population metrics.
		
		self.log( "Updating population metrics." );
		
		self.update_population_metrics( );
		
		# Adapt crossover and mutation probabilities if using self-adaptation.
		
		if ( self.use_self_adaptation == True ):
			
			self.log( "Adapting crossover/mutation probabilities." );
			
			self.adapt_crossover_and_mutation_probabilities( );
			
		# Calculate current population makeup.
		
		self.log( "Computing population makeup." );
		
		self.compute_population_makeup( );
		
		# Create a temporary population to store newly created generation.
		
		self.log( "Creating empty new population." );
		
		new_population = [ ];
		
		# Allow the top N elite to pass into the next generation.
		
		self.log( "Performing elitism." );

		self.elitism_operator( new_population );
		
		# Perform crossover and mutation separately?
		
		if ( not self.perform_crossover_and_mutation_sequentially ):
			
			self.log( "Performing crossover and mutation separately." );
			
			self.log( "Entering the loop." );

			# Now we enter the GA loop.

			# Repeat until a new population is generated.
			
			while ( len( new_population ) < self.population_size ):
				
				# Perform crossover and mutation separately.
				
				# Try to generate an offspring via crossover first.
				
				self.total_number_of_crossover_attempts += 1;
				
				# Select two genome indexes.
				
				parents = self.selection_operator( 2 );
				
				crossover_offspring = self.crossover_operator( parents[ 0 ], parents[ 1 ] );
				
				if ( crossover_offspring != 0 ):
					
					self.log( "Adding crossover offspring." );

					new_population.append( crossover_offspring );
					
					self.total_number_of_crossovers += 1;
				
				# There is the possibility of adding up to two 
				# offspring per while loop.
				# Don't create more than the population size.
				
				if ( len( new_population ) == self.population_size ):
					
					break;
				
				# Try to generate an offspring via mutation second.
				
				self.total_number_of_mutation_attempts += 1;
				
				# Select one genome index.
				
				parent = self.selection_operator( 1 );
				
				mutation_offspring = self.mutation_operator( parent[ 0 ] );
				
				if ( mutation_offspring != 0 ):
					
					self.log( "Adding mutation offspring." );
					
					new_population.append( mutation_offspring );
					
					self.total_number_of_mutations += 1;

			assert len( new_population ) == self.population_size, "New population size does not equal population size setting.";

			# Finished so assign new pop to the current population.
			
			self.population = [ ];
			self.population = copy.deepcopy( new_population );
			new_population  = [ ];
		
		else: # Perform crossover and mutation in sequence.
			
			self.log( "Performing crossover and mutation in sequence." );
			
			self.log( "Entering the loop." );
			
			# Now we enter the GA loop.

			# Repeat until a new population is generated.
			
			while ( len( new_population ) < self.population_size ):
			
				# Attempt crossover and then mutation in sequence.
				
				parents   = self.selection_operator( 2 );
				
				self.log( "Parents selected." );
				
				self.log( str( parents ) );
				
				offspring = self.crossover_then_mutate_operator( parents[ 0 ], parents[ 1 ] );
				
				if ( offspring != 0 ):
					
					self.log( "Adding first offspring." );
					
					# First offspring.
					
					if ( offspring[ "one" ].created_by == 1 ):
						
						self.log( "Adding crossover offspring." );
						
						self.total_number_of_crossovers         += 1;
						self.total_number_of_crossover_attempts += 1;
						self.total_number_of_mutation_attempts  += 1;
						
						new_population.append( offspring[ "one" ] );
					
					elif ( offspring[ "one" ].created_by == 2 ):
						
						self.log( "Adding mutation offspring." );
						
						self.total_number_of_mutations          += 1;
						self.total_number_of_crossover_attempts += 1;
						self.total_number_of_mutation_attempts  += 1;
						
						new_population.append( offspring[ "one" ] );
					
					elif ( offspring[ "one" ].created_by == 3 ):
						
						self.log( "Adding crossed over and mutated offspring." );
						
						self.total_number_of_crossovers         += 1;
						self.total_number_of_mutations          += 1;
						self.total_number_of_crossover_attempts += 1;
						self.total_number_of_mutation_attempts  += 1;
						
						new_population.append( offspring[ "one" ] );
					
					# Old population size should match this new population size.
					
					if ( len( new_population ) == self.population_size ):
						
						break;
					
					self.log( "Adding second offspring." );
					
					# Second offspring.
					
					if ( offspring[ "two" ].created_by == 1 ):
						
						self.log( "Adding crossover offspring." );
						
						self.total_number_of_crossovers         += 1;
						self.total_number_of_crossover_attempts += 1;
						self.total_number_of_mutation_attempts  += 1;
						
						new_population.append( offspring[ "two" ] );
					
					elif ( offspring[ "two" ].created_by == 2 ):
						
						self.log( "Adding mutation offspring." );
						
						self.total_number_of_mutations          += 1;
						self.total_number_of_crossover_attempts += 1;
						self.total_number_of_mutation_attempts  += 1;
						
						new_population.append( offspring[ "two" ] );
					
					elif ( offspring[ "two" ].created_by == 3 ):
						
						self.log( "Adding crossed over and mutated offspring." );
						
						self.total_number_of_crossovers         += 1;
						self.total_number_of_mutations          += 1;
						self.total_number_of_crossover_attempts += 1;
						self.total_number_of_mutation_attempts  += 1;
						
						new_population.append( offspring[ "two" ] );
			
			assert len( new_population ) == self.population_size, "New population size does not equal population size setting.";

			# Finished so assign new pop to the current population.
			
			self.population = [ ];
			self.population = copy.deepcopy( new_population );
			new_population  = [ ];
		
		# Calculate the observed rates.
		
		self.observed_crossover_rate = self.total_number_of_crossovers / self.total_number_of_crossover_attempts;
		self.observed_mutation_rate  = self.total_number_of_mutations  / self.total_number_of_mutation_attempts;
		
		self.log( "Observed cross/mut rates." );
		
		self.log( str( self.observed_crossover_rate ) + " " + str( self.observed_mutation_rate ) );
		
		# Advance generation counter.
		
		self.generation_number += 1;
		
'''

The BBAutoTune object.

'''

class BBAutoTune( ):
	
	def __init__( self, ga, dbm ):
		
		# The genetic algorithm and the database manager.
		
		self.ga  = ga;
		self.dbm = dbm;
		
		# The current genome being evaluated.
		
		self.current_genome = 0;
		
		# Log debug statements.
		
		self.debug = False
		
		self.log_file_name = "";
		
		# Open a browser window to the GA monitor.
		
		self.open_ga_monitor_browser_window = False;
		
		# Load in real robot data.
		
		real_forward_x_primes = pickle.load( open( get_scripts_location( ) + "data/real_robot_motion/forward/x_p_values.pkl", "rb" ) );
		real_forward_y_primes = pickle.load( open( get_scripts_location( ) + "data/real_robot_motion/forward/y_p_values.pkl", "rb" ) );
		real_forward_t_primes = pickle.load( open( get_scripts_location( ) + "data/real_robot_motion/forward/t_p_values.pkl", "rb" ) );
		
		real_forward_motion = [ ];

		for i in range( len( real_forward_x_primes ) ):
			
			x = real_forward_x_primes[ i ];
			y = real_forward_y_primes[ i ];
			t = real_forward_t_primes[ i ];
			
			real_forward_motion.append( 
				
				[ x, y, t ]
				
			);
			
		real_forward_motion = numpy.array( real_forward_motion );
		
		# Calculate the robust covariance matrix and the robust mean (location).
		
		self.mcd_fitted = sklearn.covariance.MinCovDet( assume_centered = False, support_fraction = 0.5 * ( len( real_forward_motion ) + 3.0 + 1.0 ) ).fit( real_forward_motion );
		
		self.rcm = self.mcd_fitted.covariance_;
		
		self.rcm_inv = numpy.linalg.inv( self.rcm );
		
		self.rm  = self.mcd_fitted.location_;
		
		# The threshold for Chi-square with 4 degrees of freedom (x,y,z,t) and an alpha value of 0.005.
		
		self.genome_fitness_threshold = math.sqrt( scipy.stats.chi2.isf( 1.0 - 0.995, 3 ) );
		
	def start( 
		
		self,
		population_size,
		max_generations,
		number_of_elite,
		crossover_probability,
		mutation_probability,
		max_torque,
		use_rank_selection,
		perform_crossover_and_mutation_sequentially,
		use_self_adaptation,
		open_ga_monitor_browser_window,
		debug
		
	):

		self.run_id = int( round( time.time( ) * 1000 ) );
		
		self.log( "Run ID." );
		
		self.log( str( self.run_id ) );
		
		self.debug = debug or False;
		
		if ( self.debug == True ):
			
			logs_location = get_scripts_location( ) + "logs/";
			
			self.log_file_name = logs_location + "log_" + str( self.run_id ) + ".log";
			
			self.ga.set_log_file_name( self.log_file_name );
			
			bpy.data.objects[ "robot_monitor" ].game.properties[ "log_file_name" ].value = self.log_file_name;
			
		self.log( "Max torque." );
		
		self.max_torque = max_torque;
		
		self.log( str( self.max_torque ) );
		
		# Pass the file name and directory where the robot 
		# monitor will record the robot's P and P'.
		
		bpy.data.objects[ "robot_monitor" ].game.properties[ "shared_data_file_name" ].value = get_scripts_location( ) + "shared_data/genome_P_P'.dat";
		
		self.log( "Connecting to the database." );
		
		self.dbm.connect_to_database( );
		
		self.log( "Starting the GA manager." );
		
		self.open_ga_monitor_browser_window = open_ga_monitor_browser_window;
		
		self.start_ga_monitor( );
		
		self.log( "Setting the GA parameters. PS MG NE CP MP URS PCMS USA." );
		
		self.log( str( population_size ) );
		self.log( str( max_generations ) );
		self.log( str( number_of_elite ) );
		self.log( str( crossover_probability ) );
		self.log( str( mutation_probability ) );
		self.log( str( use_rank_selection ) );
		self.log( str( perform_crossover_and_mutation_sequentially ) );
		self.log( str( use_self_adaptation ) );
		
		self.ga.set_population_size( population_size );
		self.ga.set_max_generations( max_generations );
		self.ga.set_number_of_elite( number_of_elite );
		self.ga.set_crossover_probability( crossover_probability );
		self.ga.set_mutation_probability( mutation_probability );
		self.ga.set_use_rank_selection( use_rank_selection );
		self.ga.set_perform_crossover_and_mutation_sequentially( perform_crossover_and_mutation_sequentially );
		self.ga.set_use_self_adaptation( use_self_adaptation );
		
		self.log( "Creating a random GA population." );
		
		self.ga.create_randomized_population( );
		
		self.log( "Setting the current genome to 0." );
		
		self.current_genome = 0;
		
		self.log( "Entering loop." );
		
		while ( self.ga.get_generation_number( ) < self.ga.get_max_generations( ) ):
			
			self.log( "Current genome." );
			
			self.log( str( self.ga.get_genome( self.current_genome ) ) );
			
			# Populate physics engine parameters.
			
			self.log( "Populating the physics engine parameters." );
		
			self.populate_physics_engine_parameters( self.ga.get_genome( self.current_genome ).get_genes( ) );
			
			# Run game engine.
			
			self.log( "Starting the game engine." );
			
			self.start_game_engine( );
			
			# Calculate current genome fitness.
			
			# Read in P=(x_pos,y_pos,z_pos,x_ori,y_ori,z_ori) and P'=(x_pos,y_pos,z_pos,x_ori,y_ori,z_ori)
			# which was recorded by the robot monitor while the game engine was running. 
			
			self.log( "Game engine stopped." );
			
			self.log( "Getting genome P and P'." );
			self.log( "x_pos , y_pos , z_pos , x_ori , y_ori , z_ori, s/e_tim" );
			
			shared_data_file = open( get_scripts_location( ) + "shared_data/genome_P_P'.dat", "r" );
			
			P = shared_data_file.readline( ).rstrip( );
			P = P.split( "," );
			P[ 0 ] = float( P[ 0 ] ); # x position.
			P[ 1 ] = float( P[ 1 ] ); # y position.
			P[ 2 ] = float( P[ 2 ] ); # z position.
			P[ 3 ] = float( P[ 3 ] ); # x orientation.
			P[ 4 ] = float( P[ 4 ] ); # y orientation.
			P[ 5 ] = float( P[ 5 ] ); # z orientation.
			P[ 6 ] = float( P[ 6 ] ); # Start time.
			
			P_prime = shared_data_file.readline( ).rstrip( );
			P_prime = P_prime.split( "," );
			P_prime[ 0 ] = float( P_prime[ 0 ] ); # x' position.
			P_prime[ 1 ] = float( P_prime[ 1 ] ); # y' position.
			P_prime[ 2 ] = float( P_prime[ 2 ] ); # z' position.
			P_prime[ 3 ] = float( P_prime[ 3 ] ); # x' orientation.
			P_prime[ 4 ] = float( P_prime[ 4 ] ); # y' orientation.
			P_prime[ 5 ] = float( P_prime[ 5 ] ); # z' orientation.
			P_prime[ 6 ] = float( P_prime[ 6 ] ); # End time.
			
			shared_data_file.close( );
			
			os.remove( get_scripts_location( ) + "shared_data/genome_P_P'.dat" );
			
			# Record simulated robot motion.
			
			simulated_robot_motion_file = open( get_scripts_location( ) + "data/simulated_robot_motion/forward/" + "srr_" + str( self.run_id ) + ".dat", "a" );
			
			write_string  = str( P[ 0 ] ) + ",";
			write_string += str( P[ 1 ] ) + ",";
			write_string += str( P[ 2 ] ) + ",";
			write_string += str( P[ 3 ] ) + ",";
			write_string += str( P[ 4 ] ) + ",";
			write_string += str( P[ 5 ] ) + ";";
			
			write_string  = str( P_prime[ 0 ] ) + ",";
			write_string += str( P_prime[ 1 ] ) + ",";
			write_string += str( P_prime[ 2 ] ) + ",";
			write_string += str( P_prime[ 3 ] ) + ",";
			write_string += str( P_prime[ 4 ] ) + ",";
			write_string += str( P_prime[ 5 ] ) + "\n";
			
			simulated_robot_motion_file.write( write_string );
			
			simulated_robot_motion_file.close( );
			
			self.log( str( P ) );
			
			self.log( str( P_prime ) );
			
			self.log( "Calculating genome fitness." );
			
			current_genome_fitness = self.calculate_genome_fitness( P, P_prime );
			
			self.log( "Genome fitness." );
			
			self.log( str( current_genome_fitness ) );
			
			self.ga.set_genome_fitness( self.current_genome, current_genome_fitness );				
			
			# Record the genome's phenotype (the physics parameters) and its eventual fitness.
			
			physics_parameters_with_fitness_file = open( get_scripts_location( ) + "data/physics_parameters_with_fitness/" + "ppwf_" + str( self.run_id ) + ".dat", "a" );
			
			physics_parameters_with_fitness_file.write( "fitness," + str( current_genome_fitness ) + "\n\n" );
			
			physics_parameters_with_fitness_file.close( );
			
			# Increase current genome + 1.
			
			self.log( "Increasing current genome count." );
			
			self.current_genome += 1;
			
			self.log( str( self.current_genome ) );
			
			# If current genome is equal to the population size.
			
			if ( self.current_genome == self.ga.get_population_size( ) ):
				
				self.log( "Evaluated all genomes in population." );
				
				# Separate recorded simulated robot motion by generation.
			
				simulated_robot_motion_file = open( get_scripts_location( ) + "data/simulated_robot_motion/forward/" + "srr_" + str( self.run_id ) + ".dat", "a" );
				
				simulated_robot_motion_file.write( "\n" );
				
				simulated_robot_motion_file.close( );
				
				self.log( "Current generation number: " + str( self.ga.get_generation_number( ) ) );
				
				# Update the population metrics.
				
				self.log( "Updating population metrics." );
			
				self.ga.update_population_metrics( );
			
				# Store the population metrics in the database.
				
				self.log( "Storing population metrics in the database." );
			
				a = str( self.ga.get_generation_number( ) );
				b = str( self.ga.get_highest_fitness( ) );
				c = str( self.ga.get_average_fitness( ) );
				d = str( self.ga.get_lowest_fitness( ) );
				e = str( self.ga.get_crossover_probability( ) );
				f = str( self.ga.get_mutation_probability( ) );
				
				mysql_string  = "INSERT INTO `population_metrics` ( `generation_number`, `highest_fitness`, `average_fitness`, `lowest_fitness`, `crossover_probability`, `mutation_probability` ) ";
				mysql_string += "VALUES( " + a + ", " + b + ", " + c + ", " + d + ", " + e + ", " + f + " );"; 
				
				self.dbm.execute( mysql_string );
				
				self.log( mysql_string );
				
				# Generate a new population.
				
				self.log( "Generating a new generation." );
				
				self.ga.generate_new_generation( );
				
				# Set current genome to 0.
				
				self.log( "Setting the current genome to 0." );
				
				self.current_genome = 0;
			
		self.log( "Exited loop." );
		
		self.log( "Stopping." );
			
		self.stop( );		
			
	def stop( self ):
		
		self.dbm.close_database_connection( );
		
		self.stop_ga_monitor( );
		
	def start_ga_monitor( self ):
		
		scripts_location = get_scripts_location( );
		
		if ( self.open_ga_monitor_browser_window == True ):
		
			self.cgi_http_server = subprocess.Popen( [ scripts_location + "cgi_http_server.py", "-w" ] );
			
		else:
			
			self.cgi_http_server = subprocess.Popen( scripts_location + "cgi_http_server.py" );
		
	def stop_ga_monitor( self ):
		
		self.cgi_http_server.kill( );
		
	def start_game_engine( self ):
		
		bpy.ops.view3d.game_start( );
		
	def log( self, log_string ):
		
		if ( self.log_file_name != "" ):
			
			log_file = open( self.log_file_name, "a+" );
			
			log_file.write( log_string + "\n" );
			
			log_file.close( );
			
	def calculate_mahalanobis_distance( self, point ):
		
		self.log( "Point." );
		
		self.log( str( point ) );
		
		md = scipy.spatial.distance.mahalanobis( point, self.rm, self.rcm_inv );
		
		md2 = md * md;
		
		return md, md2;
	
	def calculate_genome_fitness( self, start, end ):
		
		# Blender returns NaN for large positions/orientations for x, y, and z.
		# If this is the case, set the fitness to some large value.
		
		# start/end structure:
		#   x_pos   0
		#   y_pos   1
		#   z_pos   2
		#   x_rot   3
		#   y_rot   4
		#   z_rot   5
		# s/e_tim   6
		
		
		fitness = 9999999999.0;
		
		for i in range( len( end ) ):
			
			if ( numpy.isnan( end[ i ] ) ):
				
				return fitness;
			
		# Only 3 dof was recorded for the real robot.
		# So assemble for the simulated robot its x' position, y' position, and z' orientation.
		
		end_trimmed = [ end[ 0 ], end[ 1 ], end[ 5 ] ];
		
		md, md2 = self.calculate_mahalanobis_distance( end_trimmed );
		
		self.log( "Genome mahalanobis distance." );
		
		self.log( str( md ) );		
		
		# Penalties?
		
		self.log( "Penalties." );
		
		# Time > 1 seconds.
		
		elapsed_time = abs( ( ( end[ 6 ] - start[ 6 ] ) / 1000.0 ) - 1.0 );
		
		self.log( "Elapsed time > 1 seconds: " + str( elapsed_time ) );
		
		# Rotation in x.
		
		rotation_x = abs( end[ 3 ] - start[ 3 ] );
		
		self.log( "X rotation: " + str( rotation_x ) );
		
		# Rotation in y.
		
		rotation_y = abs( end[ 4 ] - start[ 4 ] );
		
		self.log( "Y rotation: " + str( rotation_y ) );
		
		# Translation in z.
		
		translation_z = abs( end[ 2 ] - start[ 2 ] );
		
		self.log( "Z translation: " + str( translation_z ) );
		
		fitness = md + elapsed_time + rotation_x + rotation_y + translation_z;
			
		return fitness;
		
	def populate_physics_engine_parameters( self, genome_genes ):
		
		self.log( "Genome genes." );
		
		self.log( str( genome_genes ) );
		
		assert len( genome_genes ) == self.ga.get_number_of_genes_per_genome( ), "Cannot populate physics engine parameters.";

		# Blender API call examples:
		#
		# bpy.data.objects["Cylinder"].game.actuators["Motion"].torque = [0,401,0];
		# bpy.data.objects["Cylinder"].game.sensors["Always"].use_tap = False;
		# bpy.ops.logic.actuator_add( type="MOTION", name="motion1", object="Cylinder");
		# bpy.data.objects["Cylinder"].game.controllers[ "Python" ].link( sensor=None, actuator=bpy.data.objects["Cylinder"].game.actuators["motion1"] );
		# bpy.data.objects["Cylinder"].game.mass = 10000.0;
		# bpy.data.scenes["Scene"].game_settings.physics_gravity;
		
		# Blender's largest number called "inf".
		# To find, set an appropriate field to a very large 
		# number and then click on the field and copy the number.
		# When clicking the field, the "inf" will turn numeric.
		
		INF = 340282346638528859811704183484516925440.0;
		
		BOOLEANS = [ False, True ];
		
		# Assumes the correct scene, wheel object, sensor, controller, and actuator names.
		# These names were set by hand in the .blend file. If they are changed, Blender
		# will throw an exception.
		
		scene          = "bbautotune";
		front_wheel_l  = "robot_1_wheel_front_L";
		front_wheel_r  = "robot_1_wheel_front_R";
		back_wheel_l   = "robot_1_wheel_back_L";
		back_wheel_r   = "robot_1_wheel_back_R";
		wheel_material = "wheel";
		actuator       = "torque_z";

		### WORLD
		
		# Gravity.
		
		#gravity = get_clamped_value( ( genome_genes[ 0 ] * 10000.0 ), 0.0, 10000.0 );
		
		gravity = get_clamped_value( ( genome_genes[ 0 ] * 15.0 ), 0.0, 100.0 );
		
		self.log( "Setting gravity." );
		
		self.log( str( gravity ) );
		
		bpy.data.scenes[ scene ].game_settings.physics_gravity = gravity;
		
		# Sub-steps.
		
		# You can input 1 up to 50. However, if only sliding the values, the value only goes from 1 to 5.
		# Not sure if this is a bug in the Blender code.
		
		sub_steps = get_clamped_value( math.floor( ( genome_genes[ 1 ] * ( 5 - 1 ) ) + 1 ), 1, 5 );
		
		self.log( "Setting sub steps." );
		
		self.log( str( sub_steps ) );
		
		bpy.data.scenes[ scene ].game_settings.physics_step_sub = sub_steps;
		
		# FPS.
		
		# Setting FPS within [1,30) makes the game engine run extremely slow so allow the GA to find a solution
		# within the range of 30 to 10000 FPS.
		
		fps = get_clamped_value( math.floor( ( genome_genes[ 2 ] * ( 10000 - 30 ) ) + 30 ), 30, 10000 );
		
		self.log( "Setting FPS." );
		
		self.log( str( fps ) );
		
		bpy.data.scenes[ scene ].game_settings.fps = fps;
		
		### Object 
		
		# Scale XYZ?
		
		'''

		scale = get_clamped_value( ( genome_genes[ 3 ] * INF ), 0.0, INF );
		
		bpy.data.objects[ front_wheel_l ].scale = [ scale, scale, scale ];
		bpy.data.objects[ front_wheel_r ].scale = [ scale, scale, scale ];
		bpy.data.objects[ back_wheel_l  ].scale = [ scale, scale, scale ];
		bpy.data.objects[ back_wheel_r  ].scale = [ scale, scale, scale ];
		
		'''
		
		### MATERIAL
		
		# Use physics?
		
		# Round returns incorrect values but converting its return value to a string does return the right value.
		# Convert only the numbers before the decimal '.' to an integer.
		
		'''

		index = int( str( round( genome_genes[ 4 ] ) ).split( "." )[ 0 ] );
		
		use_material_physics = BOOLEANS[ index ];
		
		self.log( "Setting use material physics." );
		
		self.log( str( use_material_physics ) );
		
		bpy.data.objects[ front_wheel_l ].material_slots[ 0 ].material.game_settings.physics = use_material_physics;
		bpy.data.objects[ front_wheel_r ].material_slots[ 0 ].material.game_settings.physics = use_material_physics;
		bpy.data.objects[ back_wheel_l  ].material_slots[ 0 ].material.game_settings.physics = use_material_physics;
		bpy.data.objects[ back_wheel_r  ].material_slots[ 0 ].material.game_settings.physics = use_material_physics;
		
		'''
		
		# Friction.
		
		material_friction = get_clamped_value( ( genome_genes[ 5 ] * 100.0 ), 0.0, 100.0 );
		
		self.log( "Setting material friction." );
		
		self.log( str( material_friction ) );
		
		bpy.data.objects[ front_wheel_l ].material_slots[ 0 ].material.physics.friction = material_friction;
		bpy.data.objects[ front_wheel_r ].material_slots[ 0 ].material.physics.friction = material_friction;
		bpy.data.objects[ back_wheel_l  ].material_slots[ 0 ].material.physics.friction = material_friction;
		bpy.data.objects[ back_wheel_r  ].material_slots[ 0 ].material.physics.friction = material_friction;
		
		# Elasticity.
		
		material_elasticity = get_clamped_value( ( genome_genes[ 6 ] ), 0.0, 1.0 );
		
		self.log( "Setting material elasticity." );
		
		self.log( str( material_elasticity ) );
		
		bpy.data.objects[ front_wheel_l ].material_slots[ 0 ].material.physics.elasticity = material_elasticity;
		bpy.data.objects[ front_wheel_r ].material_slots[ 0 ].material.physics.elasticity = material_elasticity;
		bpy.data.objects[ back_wheel_l  ].material_slots[ 0 ].material.physics.elasticity = material_elasticity;
		bpy.data.objects[ back_wheel_r  ].material_slots[ 0 ].material.physics.elasticity = material_elasticity;
		
		### PHYSICS
		
		# Type?
		
		'''

		PHYSICS_TYPES = [ "NO_COLLISION", "STATIC", "DYNAMIC", "RIGID_BODY", "SOFT_BODY", "OCCLUDE", "SENSOR", "NAVMESH", "CHARACTER" ];
		
		physics_type = get_clamped_value( math.floor( genome_genes[ 7 ] * len( PHYSICS_TYPES ) ), 0, len( PHYSICS_TYPES ) - 1 );
		
		physics_type = PHYSICS_TYPES[ physics_type ];
		
		bpy.data.objects[ front_wheel_l ].game.physics_type = physics_type;
		bpy.data.objects[ front_wheel_r ].game.physics_type = physics_type; 
		bpy.data.objects[ back_wheel_l  ].game.physics_type = physics_type; 
		bpy.data.objects[ back_wheel_r  ].game.physics_type = physics_type; 
		
		'''
		
		# Ghost?
		
		'''
		
		index = int( str( round( genome_genes[ 8 ] ) ).split( "." )[ 0 ] );
		
		use_ghost = BOOLEANS[ index ];		
		
		bpy.data.objects[ front_wheel_l ].game.use_ghost = use_ghost;
		bpy.data.objects[ front_wheel_r ].game.use_ghost = use_ghost;
		bpy.data.objects[ back_wheel_l  ].game.use_ghost = use_ghost;
		bpy.data.objects[ back_wheel_r  ].game.use_ghost = use_ghost;
		
		'''
		
		# Mass.
		
		#mass = get_clamped_value( ( genome_genes[ 9 ] * ( 10000.0 - 0.01 ) ) + 0.010, 0.010, 10000.0 );
		
		mass = get_clamped_value( ( genome_genes[ 9 ] * ( 15.0 - 0.010 ) ) + 0.010, 0.010, 15.0 );
		
		self.log( "Setting mass." );
		
		self.log( str( mass ) );
		
		bpy.data.objects[ front_wheel_l ].game.mass = mass;
		bpy.data.objects[ front_wheel_r ].game.mass = mass;
		bpy.data.objects[ back_wheel_l  ].game.mass = mass;
		bpy.data.objects[ back_wheel_r  ].game.mass = mass;
		
		# Form factor?
		
		'''
		
		form_factor = get_clamped_value( ( genome_genes[ 10 ] ), 0.0, 1.0 );
		
		self.log( "Setting form factor." );
		
		self.log( str( form_factor ) );
		
		bpy.data.objects[ front_wheel_l ].game.form_factor = form_factor;
		bpy.data.objects[ front_wheel_r ].game.form_factor = form_factor;
		bpy.data.objects[ back_wheel_l  ].game.form_factor = form_factor;
		bpy.data.objects[ back_wheel_r  ].game.form_factor = form_factor;
		
		'''
		
		# Velocity maximum.
		
		velocity_max = get_clamped_value( ( genome_genes[ 11 ] * 1000.0 ), 0.0, 1000.0 );
		
		self.log( "Setting velocity max." );
		
		self.log( str( velocity_max ) );
		
		bpy.data.objects[ front_wheel_l ].game.velocity_max = velocity_max;
		bpy.data.objects[ front_wheel_r ].game.velocity_max = velocity_max;
		bpy.data.objects[ back_wheel_l  ].game.velocity_max = velocity_max;
		bpy.data.objects[ back_wheel_r  ].game.velocity_max = velocity_max;
		
		# Damping translation.
		
		damping = get_clamped_value( ( genome_genes[ 12 ] ), 0.0, 1.0 );
		
		self.log( "Setting damping translation." );
		
		self.log( str( damping ) );
		
		bpy.data.objects[ front_wheel_l ].game.damping = damping;
		bpy.data.objects[ front_wheel_r ].game.damping = damping;
		bpy.data.objects[ back_wheel_l  ].game.damping = damping;
		bpy.data.objects[ back_wheel_r  ].game.damping = damping;
		
		# Damping rotation.
		
		rotation_damping = get_clamped_value( ( genome_genes[ 13 ] ), 0.0, 1.0 );
		
		self.log( "Setting rotation damping." );
		
		self.log( str( rotation_damping ) );
		
		bpy.data.objects[ front_wheel_l ].game.rotation_damping = rotation_damping;
		bpy.data.objects[ front_wheel_r ].game.rotation_damping = rotation_damping;
		bpy.data.objects[ back_wheel_l  ].game.rotation_damping = rotation_damping;
		bpy.data.objects[ back_wheel_r  ].game.rotation_damping = rotation_damping;
		
		# Use collision bounds?
		
		'''
		
		index = int( str( round( genome_genes[ 14 ] ) ).split( "." )[ 0 ] );
		
		use_collision_bounds = BOOLEANS[ index ];
		
		self.log( "Setting use collision bounds." );
		
		self.log( str( use_collision_bounds ) );
		
		bpy.data.objects[ front_wheel_l ].game.use_collision_bounds = use_collision_bounds;
		bpy.data.objects[ front_wheel_r ].game.use_collision_bounds = use_collision_bounds;
		bpy.data.objects[ back_wheel_l  ].game.use_collision_bounds = use_collision_bounds;
		bpy.data.objects[ back_wheel_r  ].game.use_collision_bounds = use_collision_bounds;
		
		'''
		
		# Collision margin?
		
		'''
		
		collision_margin = get_clamped_value( ( genome_genes[ 15 ] ), 0.0, 1.0 );
		
		self.log( "Setting collision margin." );
		
		self.log( str( collision_margin ) );
		
		bpy.data.objects[ front_wheel_l ].game.collision_margin = collision_margin;
		bpy.data.objects[ front_wheel_r ].game.collision_margin = collision_margin;
		bpy.data.objects[ back_wheel_l  ].game.collision_margin = collision_margin;
		bpy.data.objects[ back_wheel_r  ].game.collision_margin = collision_margin;
		
		'''
		
		# Collision bound type.
		
		#COLLISION_BOUNDS_TYPES = [ "TRIANGLE_MESH", "CONVEX_HULL", "CONE", "CYLINDER", "SPHERE", "BOX", "CAPSULE" ];
		
		COLLISION_BOUNDS_TYPES = [ "TRIANGLE_MESH", "CONVEX_HULL", "CYLINDER", "SPHERE" ];
		
		collision_bounds_type = get_clamped_value( math.floor( genome_genes[ 16 ] * len( COLLISION_BOUNDS_TYPES ) ), 0, len( COLLISION_BOUNDS_TYPES ) - 1 );
		
		collision_bounds_type = COLLISION_BOUNDS_TYPES[ collision_bounds_type ];
		
		self.log( "Setting collision bounds type." );
		
		self.log( str( collision_bounds_type ) );
		
		bpy.data.objects[ front_wheel_l ].game.collision_bounds_type = collision_bounds_type;
		bpy.data.objects[ front_wheel_r ].game.collision_bounds_type = collision_bounds_type; 
		bpy.data.objects[ back_wheel_l  ].game.collision_bounds_type = collision_bounds_type; 
		bpy.data.objects[ back_wheel_r  ].game.collision_bounds_type = collision_bounds_type; 
		
		### LOGIC BRICKS
		
		# Torque.
		
		#torque_z = get_clamped_value( ( -INF + ( genome_genes[ 17 ] * ( INF + INF ) ) ), -INF, INF );
		
		torque_z = get_clamped_value( genome_genes[ 17 ] * self.max_torque, 0.0, self.max_torque );
		
		self.log( "Setting torque_z." );
		
		self.log( str( torque_z ) );
		
		# In order to make the collision_bounds_type "CYLINDER" feasible, the wheel had to be rotated in model
		# space by -90deg around the x-axis. This allows the cylinder shape to coincide with the wheel shape.
		# Otherwise, if the wheel is unrotated, the cylinder bounds' flat sides reside at the rounded sides
		# of the wheel. Imagine standing a tire up, putting a tube over it and rolling the wheel.
		# Thus, in local space, applying torque to the wheels must be done around the z-axis since in local space,
		# the z-axis points out of the wheel hub.
		
		bpy.data.objects[ front_wheel_l ].game.actuators[ actuator ].use_local_torque = True;
		bpy.data.objects[ front_wheel_r ].game.actuators[ actuator ].use_local_torque = True;
		bpy.data.objects[ back_wheel_l  ].game.actuators[ actuator ].use_local_torque = True;
		bpy.data.objects[ back_wheel_r  ].game.actuators[ actuator ].use_local_torque = True;
		
		bpy.data.objects[ front_wheel_l ].game.actuators[ actuator ].torque = [ 0, 0, torque_z ];
		bpy.data.objects[ front_wheel_r ].game.actuators[ actuator ].torque = [ 0, 0, torque_z ];
		bpy.data.objects[ back_wheel_l  ].game.actuators[ actuator ].torque = [ 0, 0, torque_z ];
		bpy.data.objects[ back_wheel_r  ].game.actuators[ actuator ].torque = [ 0, 0, torque_z ];
		
		# Record the genome's phenotype (the physics parameters) and its eventual fitness.
		
		physics_parameters_with_fitness_file = open( get_scripts_location( ) + "data/physics_parameters_with_fitness/" + "ppwf_" + str( self.run_id ) + ".dat", "a" ); 
		
		physics_parameters_with_fitness_file.write( "gravity," + str( gravity ) + "\n" );
		physics_parameters_with_fitness_file.write( "sub_steps," + str( sub_steps ) + "\n" );
		physics_parameters_with_fitness_file.write( "fps," + str( fps ) + "\n" );
		#physics_parameters_with_fitness_file.write( "scale," + str( scale ) + "\n" );
		#physics_parameters_with_fitness_file.write( "use_material_physics," + str( use_material_physics ) + "\n" );
		physics_parameters_with_fitness_file.write( "material_friction," + str( material_friction ) + "\n" );
		physics_parameters_with_fitness_file.write( "material_elasticity," + str( material_elasticity ) + "\n" );
		#physics_parameters_with_fitness_file.write( "physics_type," + str( physics_type ) + "\n" );
		#physics_parameters_with_fitness_file.write( "use_ghost," + str( use_ghost ) + "\n" );
		physics_parameters_with_fitness_file.write( "mass," + str( mass ) + "\n" );
		#physics_parameters_with_fitness_file.write( "form_factor," + str( form_factor ) + "\n" );
		physics_parameters_with_fitness_file.write( "velocity_max," + str( velocity_max ) + "\n" );
		physics_parameters_with_fitness_file.write( "damping," + str( damping ) + "\n" );
		physics_parameters_with_fitness_file.write( "rotation_damping," + str( rotation_damping ) + "\n" );
		#physics_parameters_with_fitness_file.write( "use_collision_bounds," + str( use_collision_bounds ) + "\n" );
		#physics_parameters_with_fitness_file.write( "collision_margin," + str( collision_margin ) + "\n" );
		physics_parameters_with_fitness_file.write( "collision_bounds_type," + str( collision_bounds_type ) + "\n" );
		physics_parameters_with_fitness_file.write( "torque_z," + str( torque_z ) + "\n" );
		
		physics_parameters_with_fitness_file.close( );
		
class Database_Manager( ):
	
	def __init__( self, database_name ):
		
		self.database_name = database_name;
		
		variables_location = get_scripts_location( ) + "variables/";
		
		database_file = open( variables_location + "database.var", "r" );
		
		self.user_name = database_file.readline( ).rstrip( );
		
		self.password  = database_file.readline( ).rstrip( );
		
		self.connection = None;
		
		self.cursor = None;
		
	def connect_to_database( self ):
		
		connection_config = {
			
			"user":              self.user_name,
			"password":          self.password,
			"database":          self.database_name,
			'raise_on_warnings': True
			
		};
		
		try:
		
			self.connection = mysql.connector.connect( **connection_config );
			
			self.cursor     = self.connection.cursor( );
			
		except Exception:
			
			print( "Database_Manager: could not open a connection to the database." );
		
	def close_database_connection( self ):
		
		try:
			
			self.connection.close( );
			
		except Exception:
			
			print( "Database_Manager: could not close the database." );
			
	def execute( self, mysql_string = None ):
		
		if mysql_string == None:
			
			pass;
			
		elif self.cursor == None:
			
			print( "Database_Manager: you must open a connection the database first." );
			
		else:
			
			self.cursor.execute( mysql_string );
			
			self.connection.commit( );
			
# Seed the random module.

random.seed( );
		
# Create the BBAutoTune object.

bbautotune = BBAutoTune( Genetic_Algorithm( ), Database_Manager( "bbautotune" ) );

# Add the bbautotune object instance to Blender.

bpy.bbautotune = bbautotune;

# Switch to the game engine in Blender.

bpy.context.scene.render.engine = "BLENDER_GAME";

# Switch to the render pane.

bpy.data.screens[ "Default" ].areas[ 1 ].spaces[ 0 ].context = "RENDER";

# Setup the robot-monitor object's python controller.

position_recorder_script_text = bpy.data.texts.load( get_scripts_location( ) + "robot_monitor.py" );

bpy.data.objects[ "robot_monitor" ].game.controllers[ 0 ].text = position_recorder_script_text;

# Register the UI panel properties, the UI panel layout, and the start button operator with blender.

bpy.utils.register_module( __name__ );
