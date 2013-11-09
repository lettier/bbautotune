'''

David Lettier (C) 2013.

http://www.lettier.com/

Blender 2.68

This script allows the paddle to follow the ball in the paddle's local space YZ plane.

'''

controller = bge.logic.getCurrentController( );
paddle = controller.owner;

scene = bge.logic.getCurrentScene( );

ball = scene.objects[ "ball" ];

paddle.worldPosition.y = ball.worldPosition.y;
paddle.worldPosition.z = ball.worldPosition.z;

