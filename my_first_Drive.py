import gpiozero
import time

robot = gpiozero.Robot(left=(17,18), right=(22,27))

for i in range(4):
	robot.forward()
	time.sleep(1)
	robot.right()
	time.sleep(0.25)

