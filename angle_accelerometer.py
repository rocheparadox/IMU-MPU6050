#Author : Roche Christopher
#File created on 21 Aug 2019 8:53 PM

# The following code is based on the assumption that no linear force is exerted on the sensor
# Assumtion2: Orientation of the craft on which the sensor is mounted is in such a way that the x - axis is pitch axis. i.e pitch happens with respect to x axis
from mpu import MPU
import math
import time



# variables
rad2deg = 57.3
# device address
device_address = 0X68

mpu6050 = MPU(device_address)

mpu6050.initialize(accelerometer_config=int('00011000',2), smplrt_div_value = 0)
accl_config_const = 2048 #2048 LSB
dt = 0.1 # 1 deka sec i.e 0.1 sec

#Restrict pitch from -90 to +90 -- enables roll to be measured from 180 to -180
restrict_pitch = True

accl_x = 0
accl_y = 0
accl_z = 0

pitch = 0
roll = 0

while True:
   
    accl_x = mpu6050.get_accl_x()
    accl_y = mpu6050.get_accl_y()
    accl_z = mpu6050.get_accl_z()

    
    if restrict_pitch:

        angle_y = math.atan2(accl_x,accl_z) * rad2deg  #calculated pitch
        angle_x = math.atan(-accl_y/math.sqrt((accl_x**2)+(accl_z**2))) * rad2deg  #Calculated roll
        
        
        
        if (abs(angle_y) > 120):
            if (abs(roll - angle_y) < 20 ) :  # 20 is not based on any calculation. It is an approximate value to stop angle_y values to shoot up when angle_x goes beyond 90 degrees
                roll = angle_y
            else:
                # retain old value
                roll = 0
                pass
        else:
            roll = angle_y
        
        pitch = angle_x
    
    else:
        #Restrict roll from 90 to -90 enables pitch to be measured from 180 to -180
        
        angle_x = math.atan2(accl_y,accl_z) * rad2deg  #calculated pitch
        angle_y = math.atan(-accl_x/math.sqrt((accl_y**2)+(accl_z**2))) * rad2deg  #Calculated roll
        
        
        
        if (abs(angle_x) > 120):
            if (abs(pitch - angle_x) < 20 ) :
                pitch = angle_x
            else:
                # retain old value
                pitch = 0
                pass
        else:
            pitch = angle_x
        
        roll = angle_y

    #print(round(accl_x, 5), round(accl_y, 5), round(accl_z, 5))
    
    print(round(roll), round(pitch))
    time.sleep(dt)