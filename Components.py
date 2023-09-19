from machine import Pin, PWM, I2C
from time import sleep
from mpu6050 import MPU
from utime import ticks_ms


LEFT_ENC = 19
RIGHT_ENC = 32

leftIR_pin = 4
rightIR_pin = 13
frontIR_pin = 5

L1 = 23
L2 = 18
R1 = 33
R2 = 25


class IR:
    def __init__(self, pin: Pin) -> None:
        self.device = Pin(pin, Pin.IN)
    
    def detected(self) -> bool:
        return not self.device.value()
    
class Nav:
    def __init__(self) -> None:
        self.__leftIR = IR(leftIR_pin)
        self.__rightIR = IR(rightIR_pin)
        self.__frontIR = IR(frontIR_pin)
        
    def wallFront(self) -> None:
        if (self.__frontIR.detected()):
            print("Wall FRONT")
        return self.__frontIR.detected()
        
    def wallLeft(self) -> None:
        if (self.__leftIR.detected()):
            print("Wall LEFT")
        return self.__leftIR.detected()
    
    def wallRight(self) -> None:
        if (self.__rightIR.detected()):
            print("Wall RIGHT")
        return self.__rightIR.detected()
    

class Encoder:
    def __init__(self, pin: Pin) -> None:
        self.__value = 0
        self.device = Pin(pin, mode=Pin.IN)
        self.device.irq(trigger=Pin.IRQ_RISING, handler=self.handle)
    
    def handle(self, pin: Pin) -> None:
        self.__value += 1
#         print(f"Value: {self.__value} | Pin {"left" if pin == Pin(19) else "right"}")
    
    def getValue(self) -> int:
        return self.__value
    
    def resetValue(self, val: int =0) -> None:
        self.__value = val


class Motor:
    def __init__(self, pin1: Pin, pin2: Pin, freq: int = 500) -> None:
        self.freq = freq
        self.forwardPin = PWM(Pin(pin1), self.freq)
        self.backwardPin = PWM(Pin(pin2), self.freq)
    
    def forward(self, speed: int = 300) -> None:
        self.forwardPin.duty(speed)
        self.backwardPin.duty(0)
        
    def stop(self) -> None:
        self.forwardPin.duty(0)
        self.backwardPin.duty(0)
        
    def backward(self, speed: int = 300) -> None:
        self.forwardPin.duty(0)
        self.backwardPin.duty(speed)
        
class Motion:
    def __init__(self, leftSpeed: int = 300, rightSpeed: int = 300) -> None:
        self.__instance = None
        self.leftSpeed = leftSpeed
        self.rightSpeed = rightSpeed
        
        self.rightMotor = Motor(R1, R2)
        self.leftMotor = Motor(L1, L2)
        
        self.leftEncoder = Encoder(LEFT_ENC)
        self.rightEncoder = Encoder(RIGHT_ENC)
        
        self.mpu = MPU(I2C(scl=Pin(21), sda=Pin(22), freq=400000))
        self.prevTime = ticks_ms()
        
        self.stop()
        
    def getInstance(self, leftSpeed: int = 300, rightSpeed: int = 300):
        if not self.__instance:
            self.__instance = Motion(leftSpeed, rightSpeed)
        else:
            return self.__instance
        
        
    def forward(self) -> None:
        self.leftEncoder.resetValue()
        self.rightEncoder.resetValue()
#         speed = 0
        while True:
#             speed += 100
#             newLeft = speed
#             newRight = speed

#             newLeft = self.leftSpeed - self.calibrateLeft() + self.calibrateRight()
#             newRight = self.rightSpeed - self.calibrateRight() + self.calibrateLeft() 
# 
#             if newLeft < 0:
#                 newLeft = 0
#             if newRight < 0:
#                 newRight = 0

            self.leftSpeed = self.leftSpeed - self.calibrateLeft() + self.calibrateRight() 
            self.rightSpeed = self.rightSpeed - self.calibrateRight() + self.calibrateLeft() 
            
            if self.leftSpeed < 0:
                self.leftSpeed = 0
            if self.rightSpeed < 0:
                self.rightSpeed = 0
                
            if self.leftSpeed >1023:
                self.leftSpeed = 1023
            if self.rightSpeed > 1023:
                self.rightSpeed = 1023
            print(f"{self.leftSpeed} {self.leftEncoder.getValue()}   |  {self.rightSpeed}  {self.rightEncoder.getValue()} ")
            
            self.leftMotor.forward(self.leftSpeed)
            self.rightMotor.forward(self.rightSpeed)
            sleep(0.08)
            if self.leftEncoder.getValue() > 20 or self.rightEncoder.getValue() >20:
                self.stop()
                break;
            
        
    
    def left(self) -> None:
        self.mpu.reset()
        
        while True:
            self.leftMotor.backward(350)
            self.rightMotor.forward(350)
            print(f"Yaw: {self.mpu.getYaw((ticks_ms() - self.prevTime)/1000)}")
            
            if abs(self.mpu.getYaw((ticks_ms() - self.prevTime)/1000)) > 105:
                self.stop()
                break
            self.prevTime = ticks_ms()
    
    def right(self) -> None:
        while True:
            self.leftMotor.forward(self.leftSpeed)
            self.rightMotor.backward(self.rightSpeed)
            
            if self.leftEncoder.getValue() == 20 or self.rightEncoder.getValue() == 20:
                self.stop()
                break;
    
    def backward(self) -> None:
        self.leftMotor.backward(self.leftSpeed)
        self.rightMotor.backward(self.rightSpeed)
        sleep(1)
        self.stop()
        
    def stop(self) -> None:
        self.leftMotor.stop()
        self.rightMotor.stop()
        
    def calibrateLeft(self) -> int:
        difference = self.leftEncoder.getValue() - self.rightEncoder.getValue()
        if(difference > 3):
            return difference * 3
        return 0
        
    def calibrateRight(self) -> int:
        difference = self.rightEncoder.getValue() - self.leftEncoder.getValue()
        if(difference > 3):
            return difference * 3
        return 0
            
    






