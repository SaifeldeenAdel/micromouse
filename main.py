from machine import Pin, PWM, I2C
from Components import Nav, Motion, Motor
from time import sleep
from utime import ticks_ms
import network
from Maze import Maze
from Mouse import Mouse
from DIRECTIONS import Directions
from mpu6050 import MPU


def main():
    connectToNetwork()
    maze = Maze(16, 16)
#     mouse = Mouse(0, 0, Directions.NORTH)
    
    nav = Nav()
#     while True:
#         updateWalls(maze, mouse, nav)
#         sleep(0.1)
#     
    motion = Motion(leftSpeed = 620, rightSpeed=650)
    motion.backward()
    sleep(0.5)
    motion.forward()
    sleep(0.5)
    motion.left()
    sleep(0.5)
#     motion.forward()
#     sleep(0.5)
    
    motion.forward()
    
#     motion.stop()
    
#     i2c = I2C(scl=Pin(21), sda=Pin(22), freq=400000)
#     mpu = MPU(i2c)
#     prev_time = ticks_ms()
#     while True:
#         curr_time = ticks_ms()
#         dt = (curr_time - prev_time) / 1000
#         
#         prev_time = curr_time
#         yaw = mpu.getYaw(dt)
#         
#         print(f"Yaw: {yaw}")
#         if yaw > 90:
#             mpu.reset()
        
    
#     
# 
#     while True: 
#         updateWalls(maze,mouse)
#         mouse.moveForward()


def updateWalls(maze: Maze, mouse: Mouse, nav: Nav) -> None:
    """Updates walls on simulator and maze data"""
    if nav.wallFront():
        print("WALL FRONT")
    if nav.wallLeft():
        print("WALL LEFT")
    if nav.wallRight():
        print("WALL RIGHT")
        
        
def connectToNetwork():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect("FAMILY_NEW.", "10001000")
        sleep(3)
    if wlan.isconnected():
        print(f"Connected -  {wlan.ifconfig()}")
    else:
        print("Failed Connection")
    

if __name__ == "__main__":
    main()




