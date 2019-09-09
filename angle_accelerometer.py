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

accl_x = 0
accl_y = 0
accl_z = 0

pitch = 0
roll = 0

while True:
    #accl_x = mpu6050.get_accl_x() - accl_x_offset
    #accl_y = mpu6050.get_accl_y() - accl_y_offset
    #accl_z = mpu6050.get_accl_z() - accl_z_offset
    
    accl_x = mpu6050.get_accl_x()
    accl_y = mpu6050.get_accl_y()
    accl_z = mpu6050.get_accl_z()
    
    #accl_x = round(mpu6050.get_accl_x(), 2)
    #accl_y = round(mpu6050.get_accl_y(), 2)
    #accl_z = round(mpu6050.get_accl_z(), 2)
    

    #accl_x = accl_x / accl_config_const 
    #accl_y = accl_y / accl_config_const
    #accl_z = accl_z / accl_config_const
    
    #total_vector = accl_x + accl_y + accl_z
    
    #print(accl_x)
    
    #angle_y = math.asin(accl_x / total_vector) * rad2deg
    #angle_x = math.asin(accl_y / total_vector) * rad2deg
    
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
    
    
    
    #lpf_x.update(angle_x)
    #lpf_y.update(angle_y)
    #lpf_z.update(accl_z)
    
    #angle_x = lpf_x.get_output()
    #angle_y = lpf_y.get_output()
    #accl_z = lpf_z.get_output()


    #print(round(accl_x, 5), round(accl_y, 5), round(accl_z, 5))
    
    print(round(pitch), round(roll))
    time.sleep(dt)