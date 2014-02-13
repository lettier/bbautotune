import sys;
import subprocess;
import os;
import bpy;
from bpy.props import *;

def initialize_ga_parameter_properties( ):
	
	bpy.types.Scene.GA_POPULATION_SIZE   = IntProperty( name = "Population Size",  description = "Population size."  );
	bpy.context.scene[ "GA_POPULATION_SIZE" ] = 10;
	
	bpy.types.Scene.GA_MAX_GENERATIONS = IntProperty( name = "Max Generations", description = "Max generations." );
	bpy.context.scene[ "GA_MAX_GENERATIONS" ] = 100;

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
	
	bpy.types.Scene.GA_DEBUG = BoolProperty( 
		
		name        = "Debug",
		description = "Show debug information."
		
	);	
	bpy.context.scene[ "GA_DEBUG" ] = False;
 
initialize_ga_parameter_properties( ); 

class GA_UI_PANEL( bpy.types.Panel ):
	
	bl_label       = "GA Properties | BBAutoTune";
	bl_space_type  = "PROPERTIES";
	bl_region_type = "WINDOW";
	bl_context     = "render";
 
	def draw( self, context ):

		self.layout.prop( context.scene, "GA_POPULATION_SIZE"       );
		self.layout.prop( context.scene, "GA_MAX_GENERATIONS"       );
		self.layout.prop( context.scene, "GA_CROSSOVER_PROBABILITY" );
		self.layout.prop( context.scene, "GA_MUTATION_PROBABILITY"  );
		self.layout.prop( context.scene, "GA_DEBUG"                 );

		self.layout.operator( "ga.start" ); 
 
class GA_UI_START_BUTTON_OPERATOR( bpy.types.Operator ):
	
	bl_idname = "ga.start";
	bl_label  = "Start"

	def execute( self, context ):
		
		ga.set_population_size( bpy.context.scene.GA_POPULATION_SIZE );
		
		ga.set_max_generations( bpy.context.scene.GA_MAX_GENERATIONS );

		ga.set_crossover_probability( bpy.context.scene.GA_CROSSOVER_PROBABILITY );
		
		ga.set_mutation_probability( bpy.context.scene.GA_MUTATION_PROBABILITY );
		
		ga.set_debug( bpy.context.scene.GA_DEBUG );
		
		print( ga.get_population_size( ) );
		
		print( ga.get_max_generations( ) );
		
		print( ga.get_crossover_probability( ) );
		
		print( ga.get_mutation_probability( ) );
		
		print( ga.get_debug( ) );
		
		ga.run_game_engine( );

		return { 'FINISHED' };   
 
class GA( ):
	
	def __init__( self ):
		
		self.population_size = 0;
		
		self.max_generations = 0;
		
		self.crossover_probability = 0.0;
		
		self.mutation_probability  = 0.0;
		
		self.debug = False;
		
	def set_population_size( self, size ):
		
		self.population_size = size;
		
	def get_population_size( self ):
		
		return self.population_size;
	
	def set_max_generations( self, maximum ):
		
		self.max_generations = maximum;
		
	def get_max_generations( self ):
		
		return self.max_generations;
		
	def set_crossover_probability( self, probability ):
		
		self.crossover_probability = probability;
		
	def get_crossover_probability( self ):
		
		return self.crossover_probability;
	
	def set_mutation_probability( self, probability ):
		
		self.mutation_probability = probability;
		
	def get_mutation_probability( self ):
		
		return self.mutation_probability;
	
	def set_debug( self, boolean ):
		
		self.debug = boolean;
		
	def get_debug( self ):
		
		return self.debug;
	
	def run_game_engine( self ):
		
		current_working_directory = os.getcwd( );		
		scripts_location = current_working_directory.rsplit( "/", 1 )[ 0 ] + "/scripts/";
		
		cgi_http_server = subprocess.Popen( scripts_location + "cgi_http_server.py" );
		
		bpy.ops.view3d.game_start( );
		
		
ga = GA( ); 

bpy.context.scene.render.engine = "BLENDER_GAME";

bpy.utils.register_module( __name__ );