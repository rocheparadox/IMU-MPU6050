#Author : Roche Christopher
#File created on 18 Aug 2019 10:04 AM

from mpu import MPU
#import time
import RPi.GPIO as GPIO

# variables
data_available = False
# device address
device_address = 0X68
interrupt_pin = 18

GPIO.setmode(GPIO.BCM)
mpu6050 = MPU(device_address)

#gyro related variables
gyro_to_angle_dt = 32.8 # 2000 / 2**16
dt = 0.01 # 1 ms


mpu6050.initialize(general_config=1, smplrt_div_value=9, gyro_config=16)
GPIO.setup(interrupt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def interrupt_callback(channel):
    # print("Interrupt Called")
    mpu6050.get_interrupt_status()
    global data_available
    data_available = True

GPIO.add_event_detect(interrupt_pin, GPIO.FALLING, callback=interrupt_callback)
print("calibrating gyroscope")

gyro_x_offset = 0


mpu6050.get_interrupt_status()
sample_count = 20
for i in range(sample_count):
    # wait here until falling edge of interrupt pin
    while not data_available:
        pass
    gyro_x_offset += mpu6050.get_gyro_x()
    data_available = False


gyro_x_offset /= sample_count
#prev_gyro_x = mpu6050.get_gyro_x()

angle_x = 0

#mpu6050.get_interrupt_status()
while True:

    if data_available:
        # print("Data available")
        data_available = False
        gyro_x = mpu6050.get_gyro_x() - gyro_x_offset 
        angle_x_dt = int(gyro_x / gyro_to_angle_dt)
        angle_x = angle_x + (angle_x_dt * dt)
        print(angle_x)
