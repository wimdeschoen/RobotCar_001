#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

# Minor edits by Matt Timmons-Brown for "Learn Robotics with Raspberry Pi"

import time
from rpi_ws281x import *
import argparse

# LED strip configuration:
LED_COUNT      = 8      # Number of LED pixels.
#LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 20     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB # Strip type and color ordering

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=100):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=1000, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=200, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=200, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

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


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            #print ('Color wipe animations.')
            #colorWipe(strip, Color(255, 0, 0))  # Red wipe
            #colorWipe(strip, Color(0, 255, 0))  # Blue wipe
            #colorWipe(strip, Color(0, 0, 255))  # Green wipe
            #print ('Theater chase animations.')
            #theaterChase(strip, Color(127, 127, 127))  # White theater chase
            #theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            #theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            #print ('Rainbow animations.')
            #rainbow(strip)
            #rainbowCycle(strip)
            #theaterChaseRainbow(strip)
            print("Headlights on")
            lights(strip, 1 , 1)
            print("Pink right")
            pink(strip, 2, 1)
            print("Headlights on")
            lights(strip, 1 , 1)
            print("Pink right")
            pink(strip, 2, 2)
            print("Backlights on")
            lights(strip, 1,2)
            time.sleep(2)
            			
    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
