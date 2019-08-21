#Author : Roche Christopher
#File created on 21 Aug 2019 8:53 PM

# The following code is based on the assumption that no linear force is exerted on the sensor
from mpu import MPU
import math
import time

# variables
rad2deg = 57.2957786
# device address
device_address = 0X68

mpu6050 = MPU(device_address)

#gyro related variables

mpu6050.initialize(accelerometer_config=0, smplrt_div_val = 0)
gyro_to_angle_dt = 0.061035156 # 4000 / 2**16
dt = 0.001 # 1 ms

accl_x = mpu6050.get_accl_x()
accl_y = mpu6050.get_accl_y()
accl_z = mpu6050.get_accl_z()

while True:
    angle_x = math.atan2(accl_y,accl_z) * rad2deg
    angle_y = math.atan(-accl_x/math.sqrt((accl_y**2)+(accl_z**2))) * rad2deg

    print(angle_x)
    print(angle_y)
    time.sleep(dt)