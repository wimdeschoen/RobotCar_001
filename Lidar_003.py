#Start of example from https://github.com/tizianofiorenzani/ros_tutorials/blob/master/laser_scanner_tfmini/src/tfmini.py
#Needs sudo to run!
#
#Standard output format of TFmini
	#Byte 0 and 1 : 0x59 (frame header
	#Byte 2 : Distance lower 8 bits
	#Byte 3 : Distance higher 8 bits
	#Byte 4	: Strength low 8 bits
	#Byte 5 : Strength high 8 bits
	#Byte 6 : Mode , 02 short distance of 07 long distance
	#Byte 7 : Spare
	#Byte 8	: Checksum low 8 bits of the cumulative sum of hte numbers of the first 8 bytes

import serial
import time


class Tfmini():
	
	def __init__(self, serial_port="/dev/ttyAMA0"):
		
		self._ser=serial.Serial(serial_port, 115200)
		if self._ser.is_open == False:
			self._ser.open()
			
		self._distance = 0
		self._strength = 0
		self._mode = 0
		self.distance_min = 30
		self.distance_max = 1200
		
	def get_data(self):
		time0=time.time()
		while True:
			count = self._ser.in_waiting
			#print("Messages in buffer: ", count) #Test to see number of messages in buffer
			distance=-1
			strength= -1
			mode=-1
			if time.time() >time0 + 1: break
			if count > 8:
				recv = self._ser.read(9)
				self._ser.reset_input_buffer()
				if recv[0] == 0x59 and recv[1] == 0x59 : # 0x59 is 'Y'
					distance = recv[2] + recv[3] * 256
					strength = recv[4] + recv[5] * 256
					mode = recv[6]
					break
		self._distance = distance
		self._strength = strength
		self._mode= mode
		return(distance)
		
	@property
	def distance(self):
		return(self._distance)
	def strength(self):
		return(self._strength)
	def mode(self):
		return(self._mode)
	def print_data_thread(self):
		if True:
			print(self.get_data())
			
	def close(self):
		if self._ != None:
			self._ser.close()
			print("Connection to tfMini is closed")

if __name__ == '__main__':
	try:
		while True:
			tfmini= Tfmini()
			tfmini.print_data_thread()
			#print("Fucntion completed!")
			#print (tfmini.strength())
			print("This is the strenght", tfmini.strength())
			print("This is the mode", tfmini.mode())
			time.sleep(0.1)
	except 	KeyboardInterrupt:
		tfmini.close()
		
						
