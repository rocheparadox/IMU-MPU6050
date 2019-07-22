#Author : Roche Christopher
#File created on 19 Jul 2019 8:55 AM

import smbus2 as smbus


bus=smbus.SMBus(1)

class MPU:

    def __init__(self, device_address):
        self.address = device_address

    def initialize(self):

        # address of some important registers
        PWR_MGMT_1=0X6b
        SMPLRT_DIV=0X19
        CONFIG=0X1A
        GYRO_CONFIG=0X1B
        INT_ENABLE=0X38

        # write data into some registers

        # write to power management register - set  "PLL with X axis gyroscope reference" as clock source
        bus.write_byte_data(self.address, PWR_MGMT_1, 1)

        # write to smplrt_div ---> Sample Rate = Gyroscope Output Rate / (1 + SMPLRT_DIV)
        bus.write_byte_data(self.address, SMPLRT_DIV, 7)

        # set the gyro configuration to 2000 degrees / second
        bus.write_byte_data(self.address, GYRO_CONFIG, 28)

        # write to interrupt enable register
        bus.write_byte_data(self.address, INT_ENABLE, 1)


    def read_raw_data(self, mem_address):

        return bus.read_byte_data(mem_address)

    def get_integrated_data(self, high_address, low_address):

        high_data=self.read_raw_data(high_address)
        low_data=self.read_raw_data(low_address)

        return ((high_data << 8) | low_data)

    def get_gyro_x(self):

        gyro_x_out_h = 0X43
        gyro_x_out_l = 0X44
        return self.get_integrated_data(gyro_x_out_h, gyro_x_out_l)

    def get_gyro_y(self):

        gyro_y_out_h = 0X45
        gyro_y_out_l = 0X46
        return self.get_integrated_data(gyro_y_out_h, gyro_y_out_l)

    def get_gyro_z(self):

        gyro_z_out_h = 0X47
        gyro_z_out_l = 0X48
        return self.get_integrated_data(gyro_z_out_h, gyro_z_out_l)

    def get_accl_x(self):

        accl_x_out_h = 0X3B
        accl_x_out_l = 0X3C
        return self.get_integrated_data(accl_x_out_h, accl_x_out_l)

    def get_accl_y(self):

        accl_y_out_h = 0X3D
        accl_y_out_l = 0X3E
        return self.get_integrated_data(accl_y_out_h, accl_y_out_l)

    def get_accl_z(self):

        accl_z_out_h = 0X3F
        accl_z_out_l = 0X40
        return self.get_integrated_data(accl_z_out_h, accl_z_out_l)

    def get_temp_data(self):
        # temperature sensor register address

        temp_out_h = 0X41
        temp_out_l = 0X42

        return self.get_integrated_data(temp_out_h, temp_out_l)

