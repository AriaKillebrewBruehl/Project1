# File: Breakout.py

from pgl import GWindow, GOval, GRect, GLabel, GCompound # Import pgl objects 
import random # Import random 

# Constants

GWINDOW_WIDTH = 360               # Width of the graphics window
GWINDOW_HEIGHT = 600              # Height of the graphics window
N_ROWS = 10                       # Number of brick rows
N_COLS = 10                       # Number of brick columns
BRICK_ASPECT_RATIO = 4 / 1        # Width to height ratio of a brick
BRICK_TO_BALL_RATIO = 3 / 2       # Ratio of brick width to ball size
BRICK_TO_PADDLE_RATIO = 2 / 3     # Ratio of brick to paddle width
BRICK_SEP = 2                     # Separation between bricks
TOP_FRACTION = 0.1                # Fraction of window above bricks
BOTTOM_FRACTION = 0.05            # Fraction of window below paddle
N_BALLS = 3                       # Number of balls in a game
TIME_STEP = 10                    # Time step in milliseconds
INITIAL_Y_VELOCITY = 3.0          # Starting y velocity downward
MIN_X_VELOCITY = 1.0              # Minimum random x velocity
MAX_X_VELOCITY = 3.0              # Maximum random x velocity

# Derived constants

BRICK_WIDTH = (GWINDOW_WIDTH - (N_COLS + 1) * BRICK_SEP) / N_COLS
BRICK_HEIGHT = BRICK_WIDTH / BRICK_ASPECT_RATIO
PADDLE_WIDTH = BRICK_WIDTH / BRICK_TO_PADDLE_RATIO
PADDLE_HEIGHT = BRICK_HEIGHT / BRICK_TO_PADDLE_RATIO
PADDLE_Y = (1 - BOTTOM_FRACTION) * GWINDOW_HEIGHT - PADDLE_HEIGHT
BALL_SIZE = BRICK_WIDTH / BRICK_TO_BALL_RATIO

# Derived constants, variable colors and objects (by Aria) 

OFFSET = (GWINDOW_WIDTH - (N_COLS*(BRICK_WIDTH) + (N_COLS-1)*(BRICK_SEP)))//2
colors = ("red", "gold", "limegreen", "deepskyblue", "darkviolet")

paddle = None
ball = None
diameter = BALL_SIZE
obj = None
greet = None
ballsmsg = None
endmsg = None
againmsg = None
timer = None
spacing = 40 # Spacing between messages 
count = 0 # Number of bricks removed  
clicks = 0 # Number of times user has clicked mouse 

gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT) # Create GWindow 

    
def setUp(): # Create display 
    global ballsmsg, N_BALLS, greet
    
    for i in range(5): # Create rows of bricks of specified colors 
        color = colors[i]
        y = (BRICK_HEIGHT+BRICK_SEP)*2*i
        
        for i in range(2):
            drawRow(100 + (BRICK_HEIGHT+BRICK_SEP)*i + y, color)

    makePaddle() # Create paddle (in setup)
    greet = GLabel("Click to Begin")
    greet.setFont("36pt 'Arial'")
    x = (GWINDOW_WIDTH - greet.getWidth())/2
    gw.add(greet, x, 2*GWINDOW_HEIGHT/3)

    
def ballsMessage():
    global ballsmsg

    ballsmsg = GLabel("Balls Remaining: " + str(N_BALLS)) # Tell player number of balls remaing
    ballsmsg.setFont("30pt 'Arial'")
    x = (GWINDOW_WIDTH - ballsmsg.getWidth())/2
    gw.add(ballsmsg, x, 2*GWINDOW_HEIGHT/3 + spacing)
      
def drawRow(y, color): # Create rows of brick 
    
    def drawBrick(x, y): # Create individual bricks 
        brick = GRect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        return brick 
    
    for i in range(N_COLS): # Create rows of bricks 
       newbrick = drawBrick(OFFSET + (BRICK_WIDTH + BRICK_SEP)*i, y)
       newbrick.setFilled(True)
       newbrick.setColor(color)  
       gw.add(newbrick)
     
def makePaddle(): #Create paddle    
    global paddle
    
    paddle = GRect((GWINDOW_WIDTH - PADDLE_WIDTH)/2, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle.setFilled(True)
    paddle.setColor("black")
    
    gw.add(paddle)
    
def mouseMotion(e): # Move paddle with mouse 
    
    lastX = e.getX()
    paddle.setLocation(lastX, PADDLE_Y)
    
    if e.getX() < 0:
        paddle.setLocation(0, PADDLE_Y)
        
    elif e.getX() > (GWINDOW_WIDTH - PADDLE_WIDTH) :
        paddle.setLocation(GWINDOW_WIDTH - PADDLE_WIDTH, PADDLE_Y)
       
def filledCircle(x, y, diameter, color):
    circle = GOval(x, y, diameter, diameter)
    circle.setFilled(True)
    circle.setFillColor(color)
    return circle
  
def createBall(): # Create ball  
    global ball
    
    ball = GCompound()
    head = filledCircle(-diameter//2, -diameter//2, diameter, "yellow")
    ball.add(head)
    mouth = filledCircle(-diameter/10, diameter/8, diameter/5, "black")
    ball.add(mouth)
    lefteye = filledCircle(-diameter/4, -diameter/4, diameter/8, "blue")
    ball.add(lefteye)
    righteye = filledCircle(diameter/8, -diameter/4, diameter/8, "blue")
    ball.add(righteye)
    '''
    return face 

    ball = GOval(GWINDOW_WIDTH//2 - (BALL_SIZE//2), 300, BALL_SIZE, BALL_SIZE)
    ball.setFilled(True)
    ball.setColor("black")
    '''
    gw.add(ball, GWINDOW_WIDTH/2, GWINDOW_HEIGHT/2)
    
def ballMove():
    global timer
    
    vy = INITIAL_Y_VELOCITY # Set initial velocity of ball 
    vx = random.uniform(MIN_X_VELOCITY, MAX_X_VELOCITY)
    if random.uniform(0, 1) < 0.5:
        vx = -vx 
    
    def step():
        nonlocal vx, vy
        global count, paddle
        
        ball.move(vx, vy) # Move ball vx, vy each step 
         
        if ball.getX() + diameter/2 >= gw.getWidth() or ball.getX() - diameter/2 <= 0.5: # Wall collisions 
            vx = -1*vx
        if ball.getY() <= 0:
            vy = -1*vy
        if ball.getY() + diameter/2 > gw.getHeight(): 
            gw.remove(ball)
            timer.stop()
            endGame()
                   
        obj = getCollidingObject() # Check what ball is colliding with 
        if obj and obj.getY() <= GWINDOW_HEIGHT/2: # Remove bricks 
            vy = -1*vy
            gw.remove(obj)
            count += 1 
            vx += (count//5)*.2 # Gradually speed up ball 
            if count == N_ROWS * N_COLS: # endGame if all bricks are removed 
                endGame()
        elif obj and obj.getY() >= GWINDOW_HEIGHT/2: # Bounce off paddle 
            ball.setLocation(ball.getX(), paddle.getY() + BALL_SIZE)
            vy = -1*vy
    
    def getCollidingObject(): # Check if ball is colliding with something 
        global obj 
        
        if gw.getElementAt(ball.getX() + diameter/2, ball.getY() + diameter/2):
            obj = gw.getElementAt(ball.getX() + diameter/2, ball.getY() + diameter/2)
            return obj
        elif gw.getElementAt(ball.getX() - diameter/2, ball.getY() + diameter/2):
            obj = gw.getElementAt(ball.getX() - diameter/2, ball.getY() + diameter/2)
            return obj
        elif gw.getElementAt(ball.getX() - diameter/2, ball.getY() - diameter/2):
            obj = gw.getElementAt(ball.getX() - diameter/2, ball.getY() - diameter/2)
            return obj
        elif gw.getElementAt(ball.getX() + diameter/2, ball.getY() - diameter/2):
            obj =  gw.getElementAt(ball.getX() + diameter/2, ball.getY() - diameter/2)
            return obj
        else:
            obj = None
            return obj  
                
    timer = gw.setInterval(step, TIME_STEP) # Timer 
   
def Play(e): # Play game (after mouse click)
    global greet, ballsmsg, endmsg, againmsg, clicks 
    clicks += 1
    
    if clicks == 1:
        gw.remove(greet) # Remove all messages when game starts 
        gw.remove(ballsmsg)
        gw.remove(endmsg)
        gw.remove(againmsg)
        ballMove() # Move ball 
        gw.addEventListener("mousemove", mouseMotion)

setUp() # Sets up only once  
def Breakout(): 
    ballsMessage()
    createBall()
    gw.addEventListener("click", Play)
    
def endGame():
    global N_BALLS, count, timer, endmsg, againmsg, clicks 
    N_BALLS -= 1
    
    if count == (N_ROWS * N_COLS): # If all bricks have been removed
        timer.stop()
        gw.remove(ball)
        endmsg = GLabel("You Won!") # Create end message, if won   
        endmsg.setFont("36pt 'Arial'")
        x = (GWINDOW_WIDTH - endmsg.getWidth())/2
        gw.add(endmsg, x, GWINDOW_HEIGHT/2)
         
    elif N_BALLS > 0:
        #gw.remove(paddle)
        clicks = 0 
        
        endmsg = GLabel("You Lost :(") # Create end message, if lost   
        endmsg.setFont("30pt 'Arial'")
        x = (GWINDOW_WIDTH - endmsg.getWidth())/2
        gw.add(endmsg, x, GWINDOW_HEIGHT*.6)
        againmsg = GLabel("Click to Play Again") # Create end message, if lost   
        againmsg.setFont("30pt 'Arial'")
        x = (GWINDOW_WIDTH - againmsg.getWidth())/2
        gw.add(againmsg, x, GWINDOW_HEIGHT*.6 + spacing)
        count = 0 
        
        Breakout()
        
    elif N_BALLS == 0:
        timer.stop()
        endmsg = GLabel("You Lost :(") # Create end message, if lost   
        endmsg.setFont("30pt 'Arial'")
        x = (GWINDOW_WIDTH - endmsg.getWidth())/2
        gw.add(endmsg, x, GWINDOW_HEIGHT/2)

        
# Startup code

if (__name__ == "__main__"):
    Breakout()
