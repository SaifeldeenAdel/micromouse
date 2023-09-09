from machine import Pin, PWM
from time import sleep

ENC1_pin = 23
ENC2_pin = 4
leftIR_pin = 27
rightIR_pin = 25
frontIR_pin = 26

L1 = PWM(Pin(32), 500)
L2 = PWM(Pin(33), 500)
R2 = PWM(Pin(13), 500)
R1 = PWM(Pin(14), 500)

slots1 = 0
slots2 = 0

def countSlots1(pin):
    global slots1
    print(f"ENC 1: {slots1}")
    slots1 += 1
    
def countSlots2(pin):
    global slots2
    print(f"ENC 2: {slots2}")
    slots2 += 1

encoder1 = Pin(ENC1_pin, mode=Pin.IN)
encoder1.irq(trigger=Pin.IRQ_RISING, handler=countSlots1)
    
encoder2 = Pin(ENC2_pin, mode=Pin.IN)
encoder2.irq(trigger=Pin.IRQ_RISING, handler=countSlots2)


leftIR = Pin(leftIR_pin, Pin.IN) 
rightIR= Pin(rightIR_pin, Pin.IN) 
frontIR = Pin(frontIR_pin, Pin.IN)


# ---------
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
    
    
    
    


