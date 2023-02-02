import time
import board
import csv
import busio
import adafruit_adxl34x
import math
#(0.0784532, -0.1176798, 8.8652116) 


def read_data(cordinates,number,li):
    x,y,z=cordinates
    d=dict()
    xx="%0.7f" % x
    yy="%0.7f" % y
    zz="%0.7f" % z
    d['x-axis']=math.trunc(float(xx)*100)
    d['y-axis']=math.trunc(float(yy)*100)
    d['z-axis']=math.trunc(float(zz)*100)
    d['number']=number
    li.append(d)
    
def write_data(l):
    n=len(l)
    seen = set()
    new_l = [] 
    for d in l:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)
    for i in new_l:
        print(i)
    print("len",len(new_l))
    return new_l


def write_csv(l,writer):
    for i in l:
        writer.writerow(i)
    # d=dict()
    # d['x-axis']= 0
    # d['y-axis']= 0
    # d['z-axis']= 0
    # d['number']= 0    
    # writer.writerow(d)
    # writer.writerow(d)

if __name__ == '__main__':    
    i2c=busio.I2C(board.SCL, board.SDA)
    ac=adafruit_adxl34x.ADXL345(i2c)
    ac.enable_motion_detection(threshold=18)
    ac.enable_tap_detection(tap_count=2,threshold=200,duration=50,latency=20,window=255)
    
    fields=['x-axis','y-axis','z-axis','number']
    csv_file=open('data.csv','w')
    writer = csv.DictWriter(csv_file, fieldnames = fields) 
    # writer.writeheader() 
    data_points = list()
    n = int(input("Enter the number to train: "))
    print("Training data set for 10 times!!!...")
    print("Double tap the pen to start reading..")
    num=0
    c=0
    while True:
        # print(ac.read())
        if ac.events['tap']:
            print("Reading input for 2 sec!!..")
            t_end = time.time() + 2
            while time.time() < t_end: #records input for 1.5 seconds
                read_data(ac.acceleration,n,data_points)
            data=write_data(data_points)
            c=c+1
            write_csv(data, writer)
            data=[]
            data_points=[]
            if(c>10):
                break
