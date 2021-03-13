import csv
import math
import time

#fieldnames= ["x_value", "total_1", "total_2"]

class write_csvData():

	def __init__(self, fileName='dataWrite.csv', fieldnames= ["pointnr" ,"Distance", "angle", "time", "x", "y"]):
		with open(fileName, 'w') as self._csv:
			print("Filename is created", fileName)
			self._csv= csv.DictWriter(self._csv, fieldnames=fieldnames)
			self._csv.writeheader()
			self.fileName= fileName
			self.fieldnames= fieldnames
	
	def writedata(self, data)	:
		with open(self.fileName, 'a') as self._csv:
			self._csv= csv.DictWriter(self._csv, fieldnames=self.fieldnames)
			print('File is opened: ', self.fileName)
			for item in data:
				self.dataPoint= item
				#item list:	
					#pointnr=	item[0] 
					#Distance = item[1]
					#angle = item[2]
					#time = item[3]
				data_collected={}
				#only X and Y values:
				print("Distance ", item[1], " angle ", item[2]  )
				coord_1= rect(item[1], item[2])
				#add to list:
				self.dataPoint = self.dataPoint + coord_1
				fieldnr=0
				for key_1 in self.fieldnames:
					data_collected.update({key_1 : self.dataPoint[fieldnr]})
					fieldnr+=1
				print("Data line collected: ", data_collected)
				#data_collected= {"x_value": coord_1[0], "total_1": coord_1[1], "total_2": res_1 }
				self._csv.writerow(data_collected)
				#print("Coordinates itemnr ", item[0], " are : x= ", coord_1[0]," y= ", coord_1[1])

def rect(r, theta):
	#theta in degrees
	#return tuple; (flaot, float): (x,y)
	x= r* math.cos(math.radians(theta))
	y= r * math.sin(math.radians(theta))
	calcCoord=[x,y]
	for calcs in calcCoord:
		if calcs > 1200.0 :
			calcs= 1200.0
		elif calcs < -1200.0 :
			calcs=-1200.0


	return calcCoord
if __name__ == '__main__':
	scanData=write_csvData(fileName='dataWrite001.csv')
	scanData.writedata([[1,1,5,6],[2,52,6,8]])
	time.sleep(1)
	scanData.writedata([[3,8,7,25]])
	scanData.writedata([[4,20,8,26]])


