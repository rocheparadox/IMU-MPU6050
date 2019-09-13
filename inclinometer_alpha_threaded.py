#Author : Roche Christopher
#File created on 13 Sep 2019 10:08 PM

from mpu import MPU
import math
import time
import threading


class inclinometer:

    def measure_angles(self):
        # variables
        rad2deg = 57.2957786
        # device address
        device_address = 0X68

        mpu6050 = MPU(device_address)
        mpu6050.initialize(gyro_config=int('00001000', 2), smplrt_div_value=1, general_config=int('00000110', 2),
                           accelerometer_config=int('00011000', 2))

        # gyro related variables
        gyro_to_angle_dt = 65.5
        accl_config_const = 2048
        dt = 0.05  # 10 ms -- Changing the sampling time will affect the output values. DO NOT DO IT!!!!!

        print("calibrating gyroscope and accelerometer")

        gyro_x_offset = 0
        gyro_y_offset = 0
        gyro_z_offset = 0

        accl_x_offset = 0
        accl_y_offset = 0
        accl_z_offset = 0

        samples = 100
        for i in range(samples):
            gyro_x_offset += mpu6050.get_gyro_x()
            gyro_y_offset += mpu6050.get_gyro_y()
            gyro_z_offset += mpu6050.get_gyro_z()

            time.sleep(0.001)

        gyro_x_offset /= samples
        gyro_y_offset /= samples
        gyro_z_offset /= samples

        accl_x = mpu6050.get_accl_x()
        accl_y = mpu6050.get_accl_y()
        accl_z = mpu6050.get_accl_z()

        accl_angle_y_offset = round(math.atan2(accl_x, accl_z) * rad2deg, 2)  # calculated pitch
        accl_angle_x_offset = round(math.atan(-accl_y / math.sqrt((accl_x ** 2) + (accl_z ** 2))) * rad2deg,
                                    2)  # Calculated roll

        print('gyroscope offsets x, y, z ', gyro_x_offset, gyro_y_offset, gyro_z_offset)

        prev_gyro_angle_x = 0
        prev_gyro_angle_y = 0
        gyro_angle_x = 0
        gyro_angle_y = 0
        gyro_angle_x_change = 0
        gyro_angle_y_change = 0

        prev_accl_angle_x = 0
        prev_accl_angle_y = 0
        accl_angle_x = 0
        accl_angle_y = 0
        accl_angle_x_change = 0
        accl_angle_y_change = 0

        trust_accl_angle_x = trust_accl_angle_y = False

        angle_x = 0
        angle_y = 0

        accl_trust_factor = 2

        prev_time = time.time()


        while True:

            # Angle calculation from gyroscope
            gyro_x = mpu6050.get_gyro_x() - gyro_x_offset
            gyro_y = mpu6050.get_gyro_y() - gyro_y_offset
            gyro_z = mpu6050.get_gyro_z() - gyro_z_offset

            gyro_angle_x_dt = int(gyro_x / gyro_to_angle_dt)
            gyro_angle_y_dt = int(gyro_y / gyro_to_angle_dt)
            gyro_angle_z_dt = int(gyro_z / gyro_to_angle_dt)

            prev_gyro_angle_x = gyro_angle_x
            prev_gyro_angle_y = gyro_angle_y
            gyro_angle_x = round(gyro_angle_x + (gyro_angle_x_dt * dt), 2)
            gyro_angle_y = round(gyro_angle_y + (gyro_angle_y_dt * dt), 2)
            # print(gyro_angle_x, gyro_angle_y)

            # Angle calculation from accelerometer
            accl_x = mpu6050.get_accl_x()
            accl_y = mpu6050.get_accl_y()
            accl_z = mpu6050.get_accl_z()

            prev_accl_angle_x = accl_angle_x
            prev_accl_angle_y = accl_angle_y
            accl_angle_y = round(math.atan2(accl_x, accl_z) * rad2deg, 2)  # calculated pitch
            accl_angle_x = round(math.atan(-accl_y / math.sqrt((accl_x ** 2) + (accl_z ** 2))) * rad2deg, 2)  # Calculated roll

            accl_angle_x -= accl_angle_x_offset
            accl_angle_y -= accl_angle_y_offset

            # print(gyro_angle_x, gyro_angle_y)
            # print(gyro_angle_x, accl_angle_x, gyro_angle_y, accl_angle_y)

            # Calculate change in angles

            gyro_angle_x_change = abs(prev_gyro_angle_x - gyro_angle_x)
            gyro_angle_y_change = abs(prev_gyro_angle_y - gyro_angle_y)

            accl_angle_x_change = abs(prev_accl_angle_x - accl_angle_x)
            accl_angle_y_change = abs(prev_accl_angle_y - accl_angle_y)

            trust_accl_angle_x = trust_accl_angle_y = False
            angle_x = gyro_angle_x
            angle_y = gyro_angle_y

            if int(gyro_angle_x_change):

                if abs(gyro_angle_x_change - accl_angle_x_change) < accl_trust_factor:
                    if abs(gyro_angle_x - accl_angle_x) < accl_trust_factor:
                        # print("X uses accl -- motion")
                        trust_accl_angle_x = True
                        # angle_x = (0.6 * gyro_angle_x) +(0.4 * accl_angle_x)
                        # gyro_angle_x = angle_x

                else:
                    # print("X -- accl moving fast")
                    pass
            else:
                # No change in gyro values
                if not int(accl_angle_x_change):
                    if abs(gyro_angle_x - accl_angle_x) < 10:
                        # print("X uses accl -- stable")
                        trust_accl_angle_x = True
                else:
                    # print("X -- accl alone moving")
                    pass

            if int(gyro_angle_y_change):

                if abs(gyro_angle_y_change - accl_angle_y_change) < accl_trust_factor:
                    if abs(gyro_angle_y - accl_angle_y) < accl_trust_factor:
                        # print("Y uses accl -- motion")
                        trust_accl_angle_y = True
                        # angle_y = (0.6 * gyro_angle_y) +(0.4 * accl_angle_y)
                        # gyro_angle_y = angle_y

                else:
                    # print("y -- accl moving fast")
                    pass
            else:
                # No change in gyro values
                if not int(accl_angle_y_change):
                    if abs(gyro_angle_y - accl_angle_y) < 10:
                        # print("Y uses accl -- stable")
                        trust_accl_angle_y = True

                else:
                    # print("Y -- accl alone moving")
                    pass

            if (trust_accl_angle_x and trust_accl_angle_y):
                angle_x = (0.6 * gyro_angle_x) + (0.4 * accl_angle_x)
                gyro_angle_x = angle_x
                angle_y = (0.6 * gyro_angle_y) + (0.4 * accl_angle_y)
                gyro_angle_y = angle_y
            '''if(trust_accl_angle_y):
                angle_y = (0.6 * gyro_angle_y) +(0.4 * accl_angle_y)
                gyro_angle_y = angle_y '''
            angle_x = round(angle_x, 2)
            angle_y = round(angle_y, 2)

            #print(angle_x, angle_y)
            self.set_angle_x(angle_x)
            self.set_angle_y(angle_y)

            while (time.time() - prev_time) < dt:
                # print("untul")
                time.sleep(0.001)
                pass
            # print(time.time() - prev_time)
            prev_time = time.time()

    def set_angle_x(self, angle_x):
        self.angle_x = angle_x

    def set_angle_y(self, angle_y):
        self.angle_y = angle_y

    def get_angle_x(self):
        return self.angle_x

    def get_angle_y(self):
        return self.angle_y

    def measure(self):
        angleThread = threading.Thread(target=self.measure_angles())
        angleThread.start()





