from machine import Pin, I2C
import utime
 
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
TEMP_OUT_H = 0x41
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

class MPU():
    def __init__(self, i2c, address=0x68):
        self.address = address
        self.i2c = i2c
        
        self.data = {
            'accel': {
                'x': 0,
                'y': 0,
                'z': 0,
            },
            'gyro': {
                'x': 0,
                'y': 0,
                'z': 0,
            }
        }
        self.yaw = 0
        self.gyroZOffset = 0
        
        self.i2c.writeto_mem(address, PWR_MGMT_1, b'\x00')
        utime.sleep_ms(100)
        self.i2c.writeto_mem(address, SMPLRT_DIV, b'\x07')
        self.i2c.writeto_mem(address, CONFIG, b'\x00')
        self.i2c.writeto_mem(address, GYRO_CONFIG, b'\x00')
        self.i2c.writeto_mem(address, ACCEL_CONFIG, b'\x00')
        
        self.calibrate()
        
     
    def read_raw_data(self, addr):
        high = self.i2c.readfrom_mem(self.address, addr, 1)[0]
        low = self.i2c.readfrom_mem(self.address, addr + 1, 1)[0]
        value = high << 8 | low
        if value > 32768:
            value = value - 65536
        return value
     
    def getRawData(self):
        temp = self.read_raw_data(TEMP_OUT_H) / 340.0 + 36.53
        accel_x = self.read_raw_data(ACCEL_XOUT_H) / 16384.0
        accel_y = self.read_raw_data(ACCEL_XOUT_H + 2) / 16384.0
        accel_z = self.read_raw_data(ACCEL_XOUT_H + 4) / 16384.0
        gyro_x = self.read_raw_data(GYRO_XOUT_H) / 131.0
        gyro_y = self.read_raw_data(GYRO_XOUT_H + 2) / 131.0
        gyro_z = self.read_raw_data(GYRO_XOUT_H + 4) / 131.0 
        
        self.data = {
            'accel': {
                'x': accel_x,
                'y': accel_y,
                'z': accel_z,
            },
            'gyro': {
                'x': gyro_x,
                'y': gyro_y,
                'z': gyro_z - self.gyroZOffset,
            }
        }
        return self.data
    
    def calibrate(self):
        print("Keep Still... Calibrating")
        sum = 0
        for i in range(300):
            sum += self.getRawData()['gyro']['z']
        self.gyroZOffset = sum / 300
    
    def reset(self):
        self.yaw = 0
        
        
    def getYaw(self, dt):
        self.getRawData()
        if abs(self.data['gyro']['z']) > 1.9:
            self.yaw += round(self.data['gyro']['z'],2) * dt
        return round(self.yaw * 2, 2)

