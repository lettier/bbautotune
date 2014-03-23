
import time;

robot_1_base = bge.logic.getCurrentController( ).owner;

if ( robot_1_base[ "init" ] == True ):
    
    bge.logic.globalDict[ "start_time" ] = time.time( ) * 1000.0;    
    
    bge.logic.globalDict[ "go_forward" ] = True;
    
    bge.logic.globalDict[ "turn" ] = False;
    
    robot_1_base[ "init" ] = False;
    
if ( bge.logic.globalDict[ "go_forward" ] ):

    if ( time.time( ) * 1000.0 - bge.logic.globalDict[ "start_time" ] > 1000.0 ):
        
        bge.logic.getCurrentScene( ).objects[ "robot_1_wheel_front_R" ].applyTorque( [ 0, 0, 0 ], True );
        bge.logic.getCurrentScene( ).objects[ "robot_1_wheel_front_L" ].applyTorque( [ 0, 0, 0 ], True );
        bge.logic.getCurrentScene( ).objects[ "robot_1_wheel_back_R" ].applyTorque(  [ 0, 0, 0 ], True );
        bge.logic.getCurrentScene( ).objects[ "robot_1_wheel_back_L" ].applyTorque(  [ 0, 0, 0 ], True );
    
        if ( len( set( bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].getLinearVelocity( False ) ) ^ set( [ 0.0, 0.0, 0.0 ] ) ) == 0 ):
            
            bge.logic.globalDict[ "start_time" ] = time.time( ) * 1000.0;
            
            bge.logic.globalDict[ "go_forward" ] = False;
            
            bge.logic.globalDict[ "turn" ] = True;
            
    else:
        
        bge.logic.getCurrentScene( ).objects[ "robot_1_wheel_front_R" ].applyTorque( [ 0, 0, 1 ], True );
        bge.logic.getCurrentScene( ).objects[ "robot_1_wheel_front_L" ].applyTorque( [ 0, 0, 1 ], True );
        bge.logic.getCurrentScene( ).objects[ "robot_1_wheel_back_R" ].applyTorque(  [ 0, 0, 1 ], True );
        bge.logic.getCurrentScene( ).objects[ "robot_1_wheel_back_L" ].applyTorque(  [ 0, 0, 1 ], True );            
            
    
if ( bge.logic.globalDict[ "turn" ] ):
 
    if ( time.time( ) * 1000.0 - bge.logic.globalDict[ "start_time" ] > 1000.0 ):
        
        bge.logic.getCurrentScene( ).objects[ "robot_1_wheel_front_R" ].applyTorque( [ 0, 0, 0 ], True );
        bge.logic.getCurrentScene( ).objects[ "robot_1_wheel_front_L" ].applyTorque( [ 0, 0, 0 ], True );
        bge.logic.getCurrentScene( ).objects[ "robot_1_wheel_back_R" ].applyTorque(  [ 0, 0, 0 ], True );
        bge.logic.getCurrentScene( ).objects[ "robot_1_wheel_back_L" ].applyTorque(  [ 0, 0, 0 ], True );
    
        if ( len( set( bge.logic.getCurrentScene( ).objects[ "robot_1_base" ].getLinearVelocity( False ) ) ^ set( [ 0.0, 0.0, 0.0 ] ) ) == 0 ):
            
            bge.logic.globalDict[ "start_time" ] = time.time( ) * 1000.0;
            
            bge.logic.globalDict[ "go_forward" ] = True;
            
            bge.logic.globalDict[ "turn" ] = False;
            
    else:
        
        bge.logic.getCurrentScene( ).objects[ "robot_1_wheel_front_R" ].applyTorque( [ 0, 0, -1.04 ], True );
        bge.logic.getCurrentScene( ).objects[ "robot_1_wheel_front_L" ].applyTorque( [ 0, 0,  1.04 ], True );
        bge.logic.getCurrentScene( ).objects[ "robot_1_wheel_back_R" ].applyTorque(  [ 0, 0, -1.04 ], True );
        bge.logic.getCurrentScene( ).objects[ "robot_1_wheel_back_L" ].applyTorque(  [ 0, 0,  1.04 ], True );  
    
    
    
    