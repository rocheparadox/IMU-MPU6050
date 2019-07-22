#Author : Roche Christopher
#File created on 22 Jul 2019 10:02 PM

from mpu import MPU
import time

# variables
# device address
device_address = 0X68

# # gyroscope register addresses
# gyro_x_out_h = 0X43
# gyro_x_out_l = 0X44
# gyro_y_out_h = 0X45
# gyro_y_out_l = 0X46
# gyro_z_out_h = 0X47
# gyro_z_out_l = 0X48
#
# # accelerometer register addresses
# accl_x_out_h = 0X3B
# accl_x_out_l = 0X3C
# accl_y_out_h = 0X3D
# accl_y_out_l = 0X3E
# accl_z_out_h = 0X3F
# accl_z_out_l = 0X40
#
# # temperature sensor register address
#
# temp_out_h = 0X41
# temp_out_h = 0X42

mpu6050 = MPU(device_address)

while True:
    gyro_x = mpu6050.get_gyro_x()
    gyro_y = mpu6050.get_gyro_y()
    gyro_z = mpu6050.get_gyro_z()

    accl_x = mpu6050.get_accl_x()
    accl_y = mpu6050.get_accl_y()
    accl_z = mpu6050.get_accl_z()

    temperature = mpu6050.get_temp_data()

    print(gyro_x, gyro_y, gyro_z, "  |  ", accl_x, accl_y, accl_z, "  |  ", temperature)

    time.sleep(0.2)
