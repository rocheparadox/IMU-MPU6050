#Author : Roche Christopher
#File created on 21 Aug 2019 9:48 PM

from mpu import MPU
import math
import time

# variables
rad2deg = 57.2957786
# device address
device_address = 0X68

mpu6050 = MPU(device_address)
mpu6050.initialize(gyro_config=int('00001000',2), smplrt_div_value = 0, general_config=6)

#gyro related variables
gyro_to_angle_dt = 65.5 # 4000 / 2**16
dt = 0.01 # 10 ms

print("calibrating gyroscope")

gyro_x_offset = 0
gyro_y_offset = 0
gyro_z_offset = 0

for i in range(2000):
    gyro_x_offset += mpu6050.get_gyro_x()
    gyro_y_offset += mpu6050.get_gyro_y()
    gyro_z_offset += mpu6050.get_gyro_z()
    time.sleep(0.001)

gyro_x_offset /= 2000
gyro_y_offset /= 2000
gyro_z_offset /= 2000

print('gyroscope offsets x, y, z ', gyro_x_offset, gyro_y_offset, gyro_z_offset)

prev_gyro_x = mpu6050.get_gyro_x()
prev_gyro_y = mpu6050.get_gyro_y()
prev_gyro_z = mpu6050.get_gyro_z()

angle_x = 0
angle_y = 0

prev_time = time.time()
while True:
    #read raw gyro values and remove the offset
    gyro_x = mpu6050.get_gyro_x() - gyro_x_offset
    gyro_y = mpu6050.get_gyro_y() - gyro_y_offset

    #convert gyro values into rate of change of angle
    angle_x_rate = int(gyro_x / gyro_to_angle_dt)
    angle_y_rate = int(gyro_y / gyro_to_angle_dt)

    #convert rate of change of angle into angle
    gyro_angle_x = round(angle_x + (angle_x_rate * dt), 2)
    gyro_angle_y = round(angle_y + (angle_y_rate * dt), 2)

    #read raw accelerometer values
    accl_x = mpu6050.get_accl_x()
    accl_y = mpu6050.get_accl_y()
    accl_z = mpu6050.get_accl_z()

    # convert acceleromter values into angles
    accl_angle_x = round(math.atan2(accl_y,accl_z) * rad2deg , 2)
    accl_angle_y = round(math.atan(-accl_x/math.sqrt((accl_y**2)+(accl_z**2))) * rad2deg, 2)


    #print(accl_x, accl_y, accl_z)
    #print(round(angle_x,2), round(angle_y,2))
    print(gyro_angle_x, accl_angle_x, gyro_angle_y, accl_angle_y)


    #print("before loop" , time.time() - p_time)
    #time.sleep(dt)
    while (time.time() - prev_time) < dt:
        pass
    #print(time.time() - prev_time)
    prev_time = time.time()



