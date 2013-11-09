'''

David Lettier (C) 2013.

http://www.lettier.com/

Blender 2.68

This script resets the ball to its original starting position and initial launch speed.

'''

controller = bge.logic.getCurrentController( );
ball = controller.owner;

if bge.logic.keyboard.events[ bge.events.RKEY ] == bge.logic.KX_INPUT_JUST_ACTIVATED:

	ball.worldPosition.x = -8;
	ball.worldPosition.y =  0;
	ball.worldPosition.z = 10;

	ball.localLinearVelocity = [ 0, 0, 0 ];

	ball.orientation = [ [ 0, 0, 0 ], [ 0, 0, 0 ], [ 0, 0, 0 ] ]; 

	ball[ "launch" ] = True;
