from adafruit_servokit import ServoKit

kit = ServoKit(channels=8)

def move_servos(command):
    if command in ["open","five"]:  # Open arm command
        kit.servo[0].angle = 180
        kit.servo[1].angle = 180
        kit.servo[2].angle = 180
        kit.servo[3].angle = 180
        kit.servo[4].angle = 180
        print("Opening or five")
    elif command in ["close"]:  # Close
        kit.servo[0].angle = 0
        kit.servo[1].angle = 0
        kit.servo[2].angle = 0
        kit.servo[3].angle = 0
        kit.servo[4].angle = 0
        print("Closing")
    elif command in ["ok"]:  # Okay
        kit.servo[0].angle = 180
        kit.servo[1].angle = 180
        kit.servo[2].angle = 0
        kit.servo[3].angle = 0
        kit.servo[4].angle = 0
        print("Okay")
    elif command in ["not ok"]:  # Not Okay
        kit.servo[0].angle = 180
        kit.servo[1].angle = 0
        kit.servo[2].angle = 0
        kit.servo[3].angle = 180
        kit.servo[4].angle = 0
        print("Bad")
    elif command in ["peace","two"]:  # Peace V
        kit.servo[0].angle = 0
        kit.servo[1].angle = 180
        kit.servo[2].angle = 180
        kit.servo[3].angle = 0
        kit.servo[4].angle = 0
        print("Peace, two")
    elif command in ["one"]:  # One
        kit.servo[0].angle = 0
        kit.servo[1].angle = 180
        kit.servo[2].angle = 0
        kit.servo[3].angle = 0
        kit.servo[4].angle = 0
        print("one")
    elif command in ["three"]:  # three
        kit.servo[0].angle = 0
        kit.servo[1].angle = 180
        kit.servo[2].angle = 180
        kit.servo[3].angle = 0
        kit.servo[4].angle = 0
        print("three")
    elif command in ["four"]:  # four
        kit.servo[0].angle = 0
        kit.servo[1].angle = 180
        kit.servo[2].angle = 180
        kit.servo[3].angle = 180
        kit.servo[4].angle = 180
        print("four")
