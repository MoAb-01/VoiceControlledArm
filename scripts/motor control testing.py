import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=8)

while True:
    for angle in range(0, 181, 5):
        kit.servo[0].angle = angle
        time.sleep(0.02)
    for angle in range(180, -1, -5):
        kit.servo[0].angle = angle
        time.sleep(0.02)

