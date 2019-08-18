#Author : Roche Christopher
#File created on 18 Aug 2019 10:04 AM

from mpu import MPU
import time

# variables
# device address
device_address = 0X68

mpu6050 = MPU(device_address)

#gyro related variables

mpu6050.initialize(gyro_configs=int('00011000',2), smplrt_div_val = 0)
gyro_to_angle_dt = 0.061035156 # 4000 / 2**16
dt = 0.001 # 1 ms

prev_gyro_x = mpu6050.get_gyro_x()
prev_gyro_y = mpu6050.get_gyro_y()
prev_gyro_z = mpu6050.get_gyro_z()

angle_x = 0
angle_y = 0
angle_z = 0

while True:
    gyro_x = mpu6050.get_gyro_x()
    gyro_y = mpu6050.get_gyro_y()
    gyro_z = mpu6050.get_gyro_z()

    angle_x_dt = gyro_x * gyro_to_angle_dt
    angle_y_dt = gyro_y * gyro_to_angle_dt
    angle_z_dt = gyro_z * gyro_to_angle_dt

    angle_x = angle_x + angle_x_dt * dt

    print(angle_x)


    time.sleep(dt)
