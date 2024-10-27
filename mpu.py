#Author : Roche Christopher
#File created on 19 Jul 2019 8:55 AM

import smbus2 as smbus


bus=smbus.SMBus(1)

class MPU:

	def __init__(self, device_address):
		self.device_address = device_address

    def initialize(self, general_config=0, gyro_config=8, accelerometer_config=0, smplrt_div_value = 7, interrupt_enable_reg=1, interrupt_pin_cfg=0b10100000):

        # address of some important registers
        PWR_MGMT_1=0X6b
        SMPLRT_DIV=0X19
        CONFIG=0X1A
        GYRO_CONFIG=0X1B
        ACCL_CONFIG=0X1C
        INT_ENABLE=0X38
        INT_PIN_CFG_ADDR=0x37
        # write data into some registers

		#write to configuration register
		bus.write_byte_data(self.device_address, CONFIG, general_config)

		# write to power management register - set  "PLL with X axis gyroscope reference" as clock source
		bus.write_byte_data(self.device_address, PWR_MGMT_1, 1)

		# write to smplrt_div ---> Sample Rate = Gyroscope Output Rate / (1 + SMPLRT_DIV)
		bus.write_byte_data(self.device_address, SMPLRT_DIV, smplrt_div_value)

		# set the gyro configuration to 2000 degrees / second -- default (when gyro_config is 28)
		print(gyro_config)
		bus.write_byte_data(self.device_address, GYRO_CONFIG, gyro_config)

		# set the accelerometer configuration to 2000 degrees / second -- default (when gyro_config is 28)
		bus.write_byte_data(self.device_address, ACCL_CONFIG, accelerometer_config)

		# write to interrupt enable register
		bus.write_byte_data(self.device_address, INT_ENABLE, interrupt_enable_config)

        # write to interrupt pin configuration register
        bus.write_byte_data(self.device_address, INT_PIN_CFG_ADDR, interrupt_pin_cfg)

    def set_general_configuration(self, configuration):
        print("setting general configuration to " + str(configuration))
        bus.write_byte_data(self.device_address, 0X1A, configuration)

	def set_gyro_configuration(self, configuration):
		print("setting gyroscope configuration to " + str(configuration))
		bus.write_byte_data(self.device_address, 0X1B, configuration)

	def set_accelerometer_configuration(self, configuration):
		print("setting accelerometer configuration to " + str(configuration))
		bus.write_byte_data(self.device_address, 0X1C, configuration)

	def set_interrupt_enable_configuration(self, configuration):
		print("Setting interrupt configuration to {configuration}")
		bus.write_byte_data(self.device_address, INT_EN_ADDR, configuration)

	def set_interrupt_pin_configuration(self, configuration):
		bus.write_byte_data(self.device_address, 0x6B, configuration)

	def read_raw_data(self, register_address):

		return bus.read_byte_data(self.device_address, register_address)

	def get_integrated_data(self, high_address, low_address):

		high_data=self.read_raw_data(high_address)
		low_data=self.read_raw_data(low_address)

		return ((high_data << 8) | low_data)
	
	def get_signed_value(self, value):
		if value > 32768 :
			return ( 65536 - value ) * (-1)
		else:
			return value

	def get_interrupt_values(self):
		INT_ADDR = 0x3A
		return self.read_raw_data(INT_ADDR)

    def get_interrupt_status(self):
        return bus.read_byte_data(self.device_address, 0x3A)

    def get_gyro_x(self):

		gyro_x_out_h = 0X43
		gyro_x_out_l = 0X44
		return self.get_signed_value(self.get_integrated_data(gyro_x_out_h, gyro_x_out_l))
		
	def get_gyro_y(self):

		gyro_y_out_h = 0X45
		gyro_y_out_l = 0X46
		return self.get_signed_value(self.get_integrated_data(gyro_y_out_h, gyro_y_out_l))

	def get_gyro_z(self):

		gyro_z_out_h = 0X47
		gyro_z_out_l = 0X48
		return self.get_integrated_data(gyro_z_out_h, gyro_z_out_l)

	def get_accl_x(self):

		accl_x_out_h = 0X3B
		accl_x_out_l = 0X3C
		return self.get_signed_value(self.get_integrated_data(accl_x_out_h, accl_x_out_l))

	def get_accl_y(self):

		accl_y_out_h = 0X3D
		accl_y_out_l = 0X3E
		return self.get_signed_value(self.get_integrated_data(accl_y_out_h, accl_y_out_l))

	def get_accl_z(self):

		accl_z_out_h = 0X3F
		accl_z_out_l = 0X40
		return self.get_signed_value(self.get_integrated_data(accl_z_out_h, accl_z_out_l))

	def get_temp_data(self):
		# temperature sensor register address

		temp_out_h = 0X41
		temp_out_l = 0X42

		return self.get_integrated_data(temp_out_h, temp_out_l)

