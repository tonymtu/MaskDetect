from motor import ServoDrive
import time
servo = ServoDrive(5)

servo.turn(500)
time.sleep(5)
servo.turn(100)