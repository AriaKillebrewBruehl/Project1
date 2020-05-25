from pgl import GWindow, GOval

import random

GWINDOW_WIDTH = 360               
GWINDOW_HEIGHT = 600 
TIME_STEP = 10  
BALL_SIZE = 30

gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)



def ball():

    ball = GOval(GWINDOW_WIDTH//2 - (BALL_SIZE//2), 300, BALL_SIZE, BALL_SIZE)
    ball.setFilled(True)
    ball.setColor("black")
    
    gw.add(ball)
    
def ballMove():
    
    ball()
    
    vy = 3 #INITIAL_Y_VELOCITY
    vx = 1 #random.uniform(MIN_X_VELOCITY, MAX_X_VELOCITY)
    if random.uniform(0, 1) < 0.5:
        vx = -vx 
    
    def step():
        nonlocal vx, vy
        
        ball.move(vx, vy)
        
        if ball.getX + BALL_SIZE >= gw.getWidth() or ball.getX <= 0:
            vx = -1*vx
            vy = -1*vy
           
        if ball.getY + BALL_SIZE >= gw.getHeight() or ball.getY <= 0:
         vx = -1*vx
         vy = -1*vy
            
            
        
        
    timer = gw.setInterval(step, TIME_STEP)
    
if (__name__ == "__main__"):
     ballMove()