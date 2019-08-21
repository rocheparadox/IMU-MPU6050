#Author : Roche Christopher
#File created on 18 Aug 2019 10:04 AM

from mpu import MPU
import time

# variables
# device address
device_address = 0X68

mpu6050 = MPU(device_address)

#gyro related variables

mpu6050.initialize(gyro_config=int('00001000',2), smplrt_div_value = 0, general_config=6)
gyro_to_angle_dt = 65.5 # 4000 / 2**16
dt = 0.006 # 1 ms

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
angle_z = 0
p_time = time.time()
while True:
    gyro_x = mpu6050.get_gyro_x() - gyro_x_offset
    gyro_y = mpu6050.get_gyro_y() - gyro_y_offset
    gyro_z = mpu6050.get_gyro_z()

    angle_x_dt = int(gyro_x / gyro_to_angle_dt)
    angle_y_dt = int(gyro_y / gyro_to_angle_dt)
    angle_z_dt = int(gyro_z / gyro_to_angle_dt)

    angle_x = angle_x + (angle_x_dt * dt)
    angle_y = angle_y + (angle_y_dt * dt)
    print(angle_x, angle_y)

    #print("before loop" , time.time() - p_time)
    #time.sleep(dt)
    while (time.time() - p_time ) < dt:
        pass
    #print(time.time() - p_time) 
    p_time = time.time()
