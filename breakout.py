# breakout.py
# Kathryn Zimmerman (kpz8) Max Senkovsky(mgs253)
# December 8, 2014
"""Primary module for Breakout application

This module contains the App controller class for the Breakout application.
There should not be any need for additional classes in this module.
If you need more classes, 99% of the time they belong in either the gameplay
module or the models module. If you are ensure about where a new class should go, 
post a question on Piazza."""
from constants import *
from gameplay import *
from game2d import *


# PRIMARY RULE: Breakout can only access attributes in gameplay.py via getters/setters
# Breakout is NOT allowed to access anything in models.py

class Breakout(GameApp):
    """Instance is a Breakout App
    
    This class extends GameApp and implements the various methods necessary 
    for processing the player inputs and starting/running a game.
    
        Method init starts up the game.
        
        Method update either changes the state or updates the Gameplay object
        
        Method draw displays the Gameplay object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the init method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Gameplay.
    Gameplay should have a minimum of two methods: updatePaddle(touch) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view     [Immutable instance of GView, it is inherited from GameApp]:
            the game view, used in drawing (see examples from class)
        _state   [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE, STATE_COMPLETE]:
            the current state of the game represented a value from constants.py
        _last    [GPoint, or None if mouse button is not pressed]:
            the last mouse position (if Button was pressed)
        _game    [GModel, or None if there is no game currently active]: 
            the game controller, which manages the paddle, ball, and bricks
    
    ADDITIONAL INVARIANTS: Attribute _game is only None if _state is STATE_INACTIVE.
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _message [GLabel]:
            the welcome message, which tells the user to click to play
        _time    [int >= 0, 0 when game state changes from STATE_INACTIVE to STATE_COUNTDOWN]:
            the frames ellapsed since state change occured
        _lives   [int >= 0 and <= NUMBER_TURNS, NUMBER_TURNS when game state changes from
                 STATE_COUNTDOWN to STATE_ACTIVE]:
            decreases by one when ball collides with bottom of screen, keeps track of
            number of lives remaining
            
    """
    

    # DO NOT MAKE A NEW INITIALIZER!
    
    # GAMEAPP METHODS
    def init(self):
        """Initialize the game state.
        
        This method is distinct from the built-in initializer __init__.
        This method is called once the game is running. You should use
        it to initialize any game specific attributes.
        
        This method should initialize any state attributes as necessary 
        to statisfy invariants. When done, set the _state to STATE_INACTIVE
        and create a message (in attribute _mssg) saying that the user should 
        press to play a game."""
        # IMPLEMENT ME
        self._state = STATE_INACTIVE
        self._message = GLabel(text='Press to Play', font_size= 36, halign= 'center', valign= 'middle', width= GAME_WIDTH, height= GAME_HEIGHT)
        self._game = None
        self._last = None
        self._time = None
        self._lives = NUMBER_TURNS

    def update(self,dt):
        """Animate a single frame in the game.
        
        It is the method that does most of the work. Of course, it should
        rely on helper methods in order to keep the method short and easy
        to read.  Some of the helper methods belong in this class, but most
        of the others belong in class Gameplay.
        
        The first thing this method should do is to check the state of the
        game. We recommend that you have a helper method for every single
        state: STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE.
        The game does different things in each state.
        
        In STATE_INACTIVE, the method checks to see if the player clicks
        the mouse (_last is None, but view.touch is not None). If so, it 
        (re)starts the game and switches to STATE_COUNTDOWN.
        
        STATE_PAUSED is similar to STATE_INACTIVE. However, instead of 
        restarting the game, it simply switches to STATE_COUNTDOWN.
        
        In STATE_COUNTDOWN, the game counts down until the ball is served.
        The player is allowed to move the paddle, but there is no ball.
        Paddle movement should be handled by class Gameplay (NOT in this class).
        This state should delay at least one second.
        
        In STATE_ACTIVE, the game plays normally.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Gameplay (NOT in this class).
        Gameplay should have methods named updatePaddle and updateBall.
        
        While in STATE_ACTIVE, if the ball goes off the screen and there
        are tries left, it switches to STATE_PAUSED.  If the ball is lost 
        with no tries left, or there are no bricks left on the screen, the
        game is over and it switches to STATE_INACTIVE.  All of these checks
        should be in Gameplay, NOT in this class.
        
        You are allowed to add more states if you wish. Should you do so,
        you should describe them here.
        
        Precondition: dt is the time since last update (a float).  This
        parameter can be safely ignored. It is only relevant for debugging
        if your game is running really slowly. If dt > 0.5, you have a 
        framerate problem because you are trying to do something too complex."""
        
        if self._state == STATE_INACTIVE:
            self._sInactive()
            
        if self._state == STATE_ACTIVE:
            self._sActive()
    
        if self._state == STATE_COUNTDOWN:
            self._sCountdown()
            
        if self._state == STATE_PAUSED:
            self._sPaused()
        
        if self._state == STATE_COMPLETE:
            self._sComplete()
            
        self._last = self.view.touch
        
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject. 
        To draw a GObject g, simply use the method g.draw(view).  It is 
        that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are
        attributes in Gameplay. In order to draw them, you either need to
        add getters for these attributes or you need to add a draw method
        to class Gameplay.  We suggest the latter.  See the example 
        subcontroller.py from class."""
        
        if self._message is not None:
            self._message.draw(self.view)
        else:
            self._game.getWall().draw(self.view)
            self._game.getPaddle().draw(self.view)
        
        if self._state == STATE_ACTIVE:
            self._game.getBall().draw(self.view)
                
    def _sInactive(self):
        """Hidden helper method which changes the game state to STATE_COUNTDOWN
        once the mouse is clicked. It sets the timer to zero and dismisses
        the welcome message"""
        
        if self._last is None and self.view.touch is not None:
            self._state = STATE_COUNTDOWN
            self._time = 0
            self._message = None
            if self._game is None:
                self._game = Gameplay(BrickWall())
    
    def _sCountdown(self):
        """Hidden helper method which keeps track of the time ellapsed in
        STATE_COUNTDOWN, calls to update paddle position, and changes the
        game state to STATE_ACTIVE 3 seconds after STATE_COUNTDOWN commences"""
        
        self._game.updatePaddle(self.view.touch)
        self._time = self._time +1
        if self._time == 180:
            self._state = STATE_ACTIVE

    def _sActive(self):
        """Hidden helper method which calls to update the position of the
        ball, paddle, and brickwall. It also checks if the game is won or
        a life was lost, and changes the game state appropriately."""
        
        self._game.moveBall(self._game.getBall())
        self._game.updatePaddle(self.view.touch)
        if self._game.noBricksLeft():
            self._state = STATE_COMPLETE
        if self._game.ballHitsBottom():
            self._state = STATE_PAUSED
            self._lives = self._lives - 1
        
    def _sPaused(self):
        """Hidden helper method which creates a message when a life is lost or
        changes the game state to STATE_COMPLETE if there are zero lives
        left. Otherwise it changes the game state to STATE_COUNTDOWN once the
        mouse is clicked. It sets the timer to zero and dismisses the message"""
        
        if self._lives == 0:
            self._state = STATE_COMPLETE
        if self._lives == 1:
            self._message = GLabel(text=`self._lives`+'Life Left, Click to Continue', font_size= 36, halign= 'center', valign= 'middle', width= GAME_WIDTH, height= GAME_HEIGHT)
        else:
            self._message = GLabel(text=`self._lives`+' Lives Left, Click to Continue', font_size= 36, halign= 'center', valign= 'middle', width= GAME_WIDTH, height= GAME_HEIGHT)
        if self._last is None and self.view.touch is not None:
            self._state = STATE_COUNTDOWN
            self._time = 0
            self._message = None
            
    def _sComplete(self):
        """Hidden helper method which creates a message when the game is over.
        The messages vary depending on whether the player won or lost."""
        
        if self._game.noBricksLeft():
            self._message = GLabel(text='Game Over: You Win!', font_size= 36, halign= 'center', valign= 'middle', width= GAME_WIDTH, height= GAME_HEIGHT)
        else:    
            self._message = GLabel(text='Game Over: You Lose', font_size= 36, halign= 'center', valign= 'middle', width= GAME_WIDTH, height= GAME_HEIGHT)
           
   