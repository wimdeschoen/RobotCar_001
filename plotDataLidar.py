import random
from itertools import count
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')


#index = count()

def animate(i, filename='lidarData.csv', fieldnames=["pointnr" ,"Distance", "angle", "time"]):
	# open CSV to get data:
	data= pd.read_csv(filename)    
	point = data[fieldnames[0]]
	x= data[fieldnames[1]]
	y= data[fieldnames[2]]
	time=data[fieldnames[3]]

	plt.cla() #clear data

    #plot data to graph
	plt.plot(x, y, label='Points')
	
	plt.legend(loc='upper left')
	plt.tight_layout()
    

ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()
