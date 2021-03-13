#Robo drive 4:
#Left and right dc motor
	#Higher start speed
#Steering aid with servo directly with wheel
	#Steering between 0 to -90°/90°
	#Avoiding before distance and turn -15°/15°
#Sonar is on servo of steering
	#
#Led strip front
	#Implemented-> lights
#Camera is mounted
	#Object recognition must be implemented


import gpiozero
import time
from rpi_ws281x import *
import argparse

#Configuration of the IO:
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
if True:	
	#Inputs
	#_________________________________________#
	#Sonar 1 on front off robot:
	#+++++++++++++++++++++++++++++++++++++++++#
	TRIG= 13
	ECHO= 19
	trigger = gpiozero.OutputDevice(TRIG)
	echo = gpiozero.DigitalInputDevice(ECHO)

	#Output movement (servo's, motors, ...)
	#_________________________________________#
	#Motor left and right
	#+++++++++++++++++++++++++++++++++++++++++#
	robot = gpiozero.Robot(left=(17,18), right=(22,23))
	#Servo for steering wheel
	#+++++++++++++++++++++++++++++++++++++++++#
	steerServo = gpiozero.AngularServo(27, min_angle= -90, max_angle=90, min_pulse_width= 5/10000, max_pulse_width= 25/10000, frame_width= 20/1000 )
	#Output signals (LED's, ....)
	#_________________________________________#
	# LED strip configuration:
	#+++++++++++++++++++++++++++++++++++++++++#
	LED_COUNT      = 8      # Number of LED pixels.

	LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
	LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
	LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
	LED_BRIGHTNESS = 20     # Set to 0 for darkest and 255 for brightest
	LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
	LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
	LED_STRIP      = ws.WS2811_STRIP_GRB # Strip type and color ordering
	# Create NeoPixel object with appropriate configuration.
	#_________________________________________#
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
	# Intialize the library (must be called once before other functions).
	#_________________________________________#
	strip.begin()



#Init of variables
#_________________________________________#
if True:
	#Speed related varibles
	#+++++++++++++++++++++++++++++++++++++++++#
	speed=0.25
	speed_Turning=0.35
	nospeed=0.0
	#Dictionary actions
	#+++++++++++++++++++++++++++++++++++++++++#
	actions= {	"Forward": (robot.forward, 0, speed),	
		"Backward": (robot.backward, 0, speed),
		"Left": (robot.left, -90, speed_Turning),
		"Right": (robot.right, 90, speed_Turning),
		"Stop": (robot.forward, 0, nospeed ),
		"Forward_Left": (robot.forward, -25, speed),
		"Forward_Right": (robot.forward, 25, speed),
	}

	#Actions:
	#+++++++++++++++++++++++++++++++++++++++++#
	actionRoboActual="Stop"

	#Angle Steering
	#+++++++++++++++++++++++++++++++++++++++++#
	actualAngle=0


#Functions
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#Inputs
#______________________________#

#Sonar on the front of the robot:
#+++++++++++++++++++++++++++++++#
def get_distance(trigger, echo):
	trigger.on()
	time.sleep(0.00001)
	trigger.off()

	pulse_start=time.time()
	pulse_end=time.time()
	timeOutEcho=False
	while echo.is_active == False and not timeOutEcho:
		pulse_start = time.time()
		timeOut= pulse_start - pulse_end
		if timeOut > 0.05:
			timeOutEcho= True
		#print("Time echo not active: ", pulse_start)
		
	while echo.is_active == True and not timeOutEcho:
		pulse_end = time.time()
		#print("Time echo active: ", pulse_end)
	if not timeOutEcho:	
		pulse_duration = pulse_end - pulse_start
		print("PulseDuration: ", pulse_duration)
		distance = 34300*(pulse_duration / 2)
		round_distance = round(distance, 1)
	else :
		round_distance = 0
		
	print("Distance: ", round_distance)
	return (round_distance)

#Processing of the inputs
#_______________________________#

#Action of the robot:
#++++++++++++++++++++++++++++++++#
def moveRobo(action):
	actionRobo = actions.get(action)
	
	#Steering
	Steer(actionRobo[1])
	time.sleep(0.2)
	#propulsion
	dcMotors(actionRobo)
	
	
	
	print("Action : ", actionRobo) 
	return()
	
#Scan of enviroment
#++++++++++++++++++++++++++++++++#
def scanSonar(trigger, echo, minAngle, maxAngle, resolution):
	#init list variable
	distList=[]
	maxdist=4
	direction="Left"
	#distList.clear
	#From 0 to maxAngle
	listItem=0
	for scanAngle in range(0, minAngle, -1):
		steerServo.angle=scanAngle
		time.sleep(0.001)
	print("To minimum angle", minAngle)
	for scanAngle in range(minAngle, maxAngle, resolution):
		distList.append([scanAngle, get_distance(trigger, echo)])
		print("Scantitem: ", distList[listItem][0], " Distance: ", distList[listItem][1])
		listItem += 1
		steerServo.angle=scanAngle
		time.sleep(0.0001)
		
	print("List", distList)	
	
	
	for item in distList:
		
		print("List item: " , item)
		if item[1] > maxdist:
			maxdist=item[1]
			print("Max distance in list ", maxdist)
			if item[0] > 0:
				direction="Right"
			else:
				direction="Left"
	print("We go ", direction, "!")
	return (direction)			
	
#Outputs
#_______________________________#	
#DC motors
#++++++++++++++++++++++++++++++++#	
def dcMotors(actionRobo):
	global actionRoboActual
	speed= actionRobo[2]
	startSpeed=0.7
	#startup of brushless dc motors	
	if (speed < startSpeed) and (actionRoboActual != actionRobo) and (speed != 0):
		for i in range(50,int(startSpeed *100),10):
			actionRobo[0](float(i)/100) 
			print("Ramp up," , i)
			time.sleep(0.05)
		for i in range(int(startSpeed*100), int(speed*100), -10):	
			actionRobo[0](float(i)/100) 
			print("Ramp down," , i)
			time.sleep(0.05)
			
	actionRobo[0](speed)
	print("Speed:", speed)
	actionRoboActual=actionRobo
	 
	return(actionRobo)
#Servo for steering
#++++++++++++++++++++++++++++++++#	
def Steer(angle):
	global actualAngle
	
	while actualAngle != angle:
		steerServo.angle=actualAngle
		if actualAngle < angle:
			actualAngle=actualAngle+1
		else:	
			actualAngle=actualAngle-1
		print("SteerAngle	:", actualAngle)
		steerServo.angle=actualAngle
		time.sleep(0.001)
	
	return(actualAngle)

#Output signals for LED strip:
#_____________________________#
#LED normal running lights
#++++++++++++++++++++++++++++++++#	
def lights(strip, mode, position):
	#position: front -> white lights, back red lights
	if position == 1:
		rangeLED1= range(2)
		rangeLED2=range(6,8)
		rangeLED3=range(2,6)
		colorLED1 = Color(255,255,255)
		colorLED2 = Color(0,0,0)
	elif position == 2:
		rangeLED1= range(3)
		rangeLED2=range(5,8)
		rangeLED3=range(3,5)
		colorLED1 = Color(255,0,0) #Color(255,99,71) #Tomato red
		colorLED2 = Color(0,0,0)#Color(128,0,128) #Violet
	for i in rangeLED1:
		strip.setPixelColor(i, colorLED1)
	for k in rangeLED2:
		strip.setPixelColor(k, colorLED1)
	for i in rangeLED3:
		strip.setPixelColor(i, colorLED2)	
	strip.show()
	time.sleep(1)
	return()
#LED when turning	
#++++++++++++++++++++++++++++++++#	
def pink(strip, mode, direction):
	#orange color : 255,131,0
	#range 4-0 right (direction = 1) or left 4-8 (direction = 2) ->
	if direction == 1:
		ledR=range(3,-1,-1)
	elif direction == 2:
		ledR=range(4,8)
	#mode = 1 : all 4 leds blink
	#mode = 2 : flow of 4 leds blinks
	if mode == 1:
		for j in range(4):
			wait_time=750
			for i in ledR:
				strip.setPixelColor(i, Color(255,131,0))
			strip.show()
			time.sleep(wait_time/1000)
			for i in ledR:
				strip.setPixelColor(i, Color(0,0,0))
			strip.show()
			time.sleep(wait_time/1000)
	elif mode == 2:
		for j in range(4):
			wait_time=150
			for i in ledR:
				strip.setPixelColor(i, Color(255,131,0))
				strip.show()
				time.sleep(wait_time/1000)
			for i in ledR:
				strip.setPixelColor(i, Color(0,0,0))
				strip.show()
				time.sleep(wait_time/1000)	
	#time.sleep(1000/1000)	
	return()	


#Main program
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
while True:
	
	dist= get_distance(trigger, echo)
	if dist <=20.0:
		print("Headlights on")
		lights(strip, 1 , 1)
		moveRobo("Stop")
		time.sleep(0.01)
		direction=scanSonar(trigger, echo,-90, 90, 1)
		if direction == "Right":
			print("Pink right")
			pink(strip, 2, 2)
			time.sleep(0.0001)
		else:
			print("Pink left")
			pink(strip, 2, 1)
			time.sleep(0.0001)
				
		moveRobo(direction)
		time.sleep(0.5)
		moveRobo("Stop")
		time.sleep(0.1)
	#elif dist <=15.0:
		#moveRobo("Right")
		#time.sleep(0.5)
	#elif dist <= 25.0:
		#print("Pink right")
		#pink(strip, 2, 2)
		#time.sleep(0.0001)
		#moveRobo("Forward_Right")
		#time.sleep(1)
	else:
		moveRobo("Forward")
		time.sleep(1)
		print("Headlights on")
		lights(strip, 1 , 1)
		#print("Pink left")
		#pink(strip, 2, 1)
		
		
		#print("Backlights on")
		#lights(strip, 1,2)
		#time.sleep(2)
		
