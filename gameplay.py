# gameplay.py
# Kathryn Zimmerman (kpz8) Max Senkovsky(mgs253)
# December 8, 2014
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Gameplay represent a single game.  If you want to restart a new game,
you are expected to make a new instance of Gameplay.

The subcontroller Gameplay manages the paddle, ball, and bricks.  These are model
objects.  The ball and the bricks are represented by classes stored in models.py.
The paddle does not need a new class (unless you want one), as it is an instance
of GRectangle provided by game2d.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Gameplay can only access attributes in models.py via getters/setters
# Gameplay is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Gameplay(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It
    animates the ball, removing any bricks as necessary.  When the game is
    won, it stops animating.  You should create a NEW instance of 
    Gameplay (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.
    
    INSTANCE ATTRIBUTES:
        _wall   [BrickWall]:  the bricks still remaining 
        _paddle [GRectangle]: the paddle to play with 
        _ball [Ball, or None if waiting for a serve]: 
            the ball to animate
        _last [GPoint, or None if mouse button is not pressed]:  
            last mouse position (if Button pressed)
        _tries  [int >= 0]:   the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you
    want to access an attribute in call Breakout. It is okay if you do, but
    you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter and/or
    setter for any attribute that you need to access in Breakout.  Only add
    the getters and setters that you need for Breakout.
    
    You may change any of the attributes above as you see fit. For example, you
    might want to make a Paddle class for your paddle.  If you make changes,
    please change the invariants above.  Also, if you add more attributes,
    put them and their invariants below.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _last    [GPoint, or None if mouse button is not pressed]:
            the last mouse position (if Button was pressed)
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getWall(self):
        """Returns: the instance attribute _wall (the bricks still remaining)"""
        return self._wall
    
    def getPaddle(self):
        """Returns: the instance attribute _paddle (the paddle to play with)"""        
        return self._paddle
    
    def getBall(self):
        """Returns: the instance attribute _ball (the ball to animate or None \
        if mouse button is not pressed)"""
        return self._ball
    
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self, brickwall):
        """Initializer: creates the paddle, ball, and wall.
        ball is a Ball object centered in the game window.
        It assigns brickwall to the wall.
        
        Precondition: brickwall is a BrickWall object"""
        
        assert isinstance(brickwall, BrickWall)
        self._wall = brickwall
        height = PADDLE_OFFSET
        self._paddle = GRectangle(x= 0, y= height, width = PADDLE_WIDTH, \
                height = PADDLE_HEIGHT, fillcolor= colormodel.BLACK, \
                linecolor=colormodel.BLACK)
        self._last = None
        self._ball = Ball(center_x = 0.5*GAME_WIDTH, center_y = 0.5*GAME_HEIGHT,\
                width = BALL_DIAMETER,height = BALL_DIAMETER,\
                fillcolor = colormodel.BLACK,linecolor = colormodel.BLACK)
    
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def draw(self,view):
        """Draws the paddle, wall objects, and the ball.
        
        Precondition: view is an immutable instance of GView"""
        
        assert isinstance(view, GView)
        self._wall.draw(view)
        self._paddle.draw(view)
        self._ball.draw(view)

    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def updatePaddle(self, current):
        """Helper function which changes the paddle position relative to the
        change in mouse position.
        
        Precondition: current is a GPoint or None"""
        
        assert isinstance(current, GPoint) or current is None
        if current is not None and self._last is not None:
            pad = self._paddle
            lastpt = self._last
            pos = pad.x + (current.x - lastpt.x) 
            if pos + PADDLE_WIDTH > GAME_WIDTH:
               pos = GAME_WIDTH - PADDLE_WIDTH
            if pos < 0:
               pos = 0
            height = PADDLE_OFFSET
            self._paddle = GRectangle(x= pos, y= height, width = PADDLE_WIDTH, \
                    height = PADDLE_HEIGHT, fillcolor= colormodel.BLACK, \
                    linecolor=colormodel.BLACK)    
        self._last = current
        
    def moveBall(self, current):
        """Helper function which updates the ball position but also changes
        the direction of the ball's velocity if it collides with the walls,
        paddle, or a brick and calls to remove the brick if the ball hits it.
        
        Precondition: current is a Ball object"""
        
        assert isinstance(current, Ball)
        self._ball.moveBall(current)
        e = self._getCollidingObject()
        if e is not None:
            a = e.contains(self._ball.x, self._ball.y + BALL_DIAMETER)
            b = e.contains(self._ball.x, self._ball.y)
            c = e.contains(self._ball.x + BALL_DIAMETER, self._ball.y)
            d = e.contains(self._ball.x + BALL_DIAMETER, self._ball.y + BALL_DIAMETER)
            if e == self._paddle and Ball().getVY() < 0:
                self._ball.paddleBounce()
            else:
                self._wall.updateBricks(e)
                #self.brickBounce(e)
                if a or d:
                    self._ball.vBounce()
                #if a and not d and not b:
                 #   self._ball.vBounce()
                if a or b:
                    self._ball.hBounce()
                    #if Ball().getVY() < 0:
                     #   self._ball.vBounce()
                if b or c:
                    self._ball.vBounce()
                if c or d:
                    self._ball.hBounce()
        
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def _getCollidingObject(self):
        """Returns: GObject that has collided with the ball
        
        This method checks the four corners of the ball, one at a 
        time. If one of these points collides with either the paddle 
        or a brick, it stops the checking immediately and returns the 
        object involved in the collision. It returns None if no 
        collision occurred."""    
        
        if self._paddle.contains(self._ball.x, self._ball.y):
            return self._paddle
        if self._paddle.contains(self._ball.x+BALL_DIAMETER,self._ball.y):
            return self._paddle
        for i in self._wall.getBricks():
            if i.contains(self._ball.x, self._ball.y + BALL_DIAMETER):
                return i
            if i.contains(self._ball.x, self._ball.y):
                return i
            if i.contains(self._ball.x + BALL_DIAMETER, self._ball.y):
                return i
            if i.contains(self._ball.x + BALL_DIAMETER, self._ball.y + BALL_DIAMETER):
                return i
        
        else:
            return None
    
    def brickBounce(self, brick):
        """dont do the specification for this yet, not sure if we will need it or
        not, trying to perfect the physics of all the different collisions the ball
        can have with the bricks still"""
        
        if Ball().getVX() < 0:
            if Ball().getVY() < 0:
                if(brick.right - self._ball.x) > (brick.top - self._ball.y):
                    self._ball.vBounce()
                else:
                    self._ball.hBounce()
            if Ball().getVY() >0:
                if (brick.right - self._ball.x) > (brick.top - self._ball.top):
                    self._ball.vBounce()
                else:
                    self._ball.hBounce()
        if Ball().getVX() > 0:
            if Ball().getVY() < 0:
                if (self._ball.right - brick.x) > (brick.top - self._ball.y):
                    self._ball.vBounce()
                else:
                    self._ball.hBounce()
            if Ball().getVY() >0:
                if (self._ball.right - brick.x) > (brick.top - self._ball.y):
                    self._ball.vBounce()
                else:
                    self._ball.hBounce()
                    
    def ballHitsBottom(self):
        """Helper method which returns True if the ball hits the bottom wall and
        it creates a new Ball object centered in the game window"""
        
        if self._ball.y <= 0:
            self._ball = Ball(center_x = 0.5*GAME_WIDTH, center_y = 0.5*GAME_HEIGHT,\
                    width = BALL_DIAMETER,height = BALL_DIAMETER,\
                    fillcolor = colormodel.BLACK,linecolor = colormodel.BLACK)
            return True 
    
    def noBricksLeft(self):
        """Helper method which returns True if no bricks remain."""
        
        if self._wall.getBricks() == []:
            return True
            
    
        
    
    
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE