from machine import Pin, PWM
from time import sleep

# --------
# IRs
#----------

def wallFront():
    # Front IR reading
    return True if not frontIR.value() else False

def wallLeft():
    # Left IR reading
    return True if not leftIR.value() else False

def wallRight():
    # Right IR reading
    return True if not rightIR.value() else False

# ----------
# Motors
#----------

def forward(left, right):
    R1.duty(right)
    R2.duty(0)
    L1.duty(left)
    L2.duty(0)
    
def backward(left, right):
    R2.duty(right)
    L2.duty(left)
    R1.duty(0)
    L1.duty(0)
    
def stop():
    L1.duty(0)
    L2.duty(0)
    R1.duty(0)
    R2.duty(0)
    
    

#-----------------------------
    
def moveForward():
    # moves forward one cell
    slots2 = slots1 = 0
    while slots1 <= 60 and slots2 <= 60:
        forward(300,300)
        
    stop()
    
        
def turnRight():
    # turning right
    pass


def turnLeft():
    # Turn left
    pass

def turnAround():
    # Turn around then hit back wall
    turnLeft()
    turnLeft()
    
    backward(300,300)
    sleep(5)
    stop()
    
    
    
    


