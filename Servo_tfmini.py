#Servo for tfmini

import gpiozero
import time
import tfmini
import write_csv

#Classes

class lidarScan():
	
	def __init__(self, pin=24):
		#Initiate the servo:
		self._lidarServo = gpiozero.AngularServo(pin, min_angle= -90, max_angle=90, min_pulse_width= 5/10000, max_pulse_width= 25/10000, frame_width= 20/1000 )
		#Initiate the Lidar sensor:
		self._laserDistance= tfmini.Tfmini()
		self.fieldnames=[ "pointnr" ,"Distance", "angle", "time", "x", "y"]
		#initiate the write to CSV:
		self._writeCSV= write_csv.write_csvData(fileName="lidarData.csv", fieldnames=self.fieldnames)
		self._scanpointnr=0
		self._listData=[self.fieldnames]
		
	def startscan(self, startAngle, endAngle, resolution, timeWait, showAngle, showDistance):	
		self._laserDistance.open()
		self._laserDistance.clearbuffer()
	
		for i in range(startAngle, (endAngle + resolution), resolution):
			self._lidarServo.angle = i
			self._scanpointnr += 1
			if showAngle :
				print("Scan angle = ", i)
			self._distance= self._laserDistance.get_data()
			if showDistance:
				print("Distance from laser: ", self._distance)
			scanData(self._scanpointnr, self._distance, i, self._listData )
			self._writeCSV.writedata([[self._scanpointnr, self._distance, i, time.time]])
		
			time.sleep(timeWait)
		#Close the laser communication
		self._laserDistance.close()
		return(self._listData)
		
	@property
	def scanpointnr(self):
		return(self._scanpointnr)
	def clearlist(self):
		self._listData=[[ "pointnr" ,"Distance", "angle", "time"]]
		print("List cleared")
		
	def endScan(self):
		self._laserDistance.close()
		print("	/n Scan stopped !"	)
		
		
		
		
#Functions		
def scanData(idnr, distance, angle, listScan):
	
	listScan.append([idnr, distance, angle, time.time()])
	return (listScan)

	
if __name__ == '__main__':
	try:
		scandata= lidarScan()
		while True:
			print("Scanning ...")
			print("Data of scan : ", scandata.startscan(-60, 60, 2, 0.1, True, True))
			print("Wait ...")
			time.sleep(2)
			scandata.clearlist()
			
	except 	KeyboardInterrupt:
		scandata.endScan()
		print("Program closed")
