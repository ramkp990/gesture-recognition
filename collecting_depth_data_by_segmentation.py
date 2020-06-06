import pyrealsense2 as rs
import numpy as np
from numpy import newaxis
import cv2
import matplotlib.pyplot as plt
import time
import csv

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 424, 240, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
profile = pipeline.start(config)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: " , depth_scale)
clipping_distance_in_meters = 1 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale
print(clipping_distance)

depth_images=[]
color_images=[]
bg_removed=[]
print("recognizing hand gesture")
time.sleep(1)
tend=time.time()+1*2
#collecting depth data
try:
	while time.time() <tend:
		frames=pipeline.wait_for_frames()
		depth_image=np.asarray(frames.get_depth_frame().get_data())
		depth_images.append(depth_image)
		time.sleep(0.00001)
		if len(depth_images)==25:
			break
finally:
	#segmenting depth data
	if len(depth_images)==25:
		for i in range(0,25):
			bg_removed.append(np.where((depth_images[i] < clipping_distance) & (depth_images[i] > 0),depth_images[i], 0))
			#print(i)
		print("hand gesture  recognized")
		leng=len(bg_removed)
		w,h=bg_removed[0].shape
		wh=w*h
		bg_removed[0].resize((wh,1))
		c=bg_removed[0]
		for i in range(1,leng):
			w,h=bg_removed[i].shape
			bg_removed[i].resize((wh,1))
			c_new=bg_removed[i]
			c=np.concatenate((c,c_new),axis=0)
		c=c.T
		#writing depth data to a csv file
		if len(bg_removed)==25:
			print("writing to file")
			with open('sundayseg.csv','a',newline='')as file:
				writer=csv.writer(file)
				writer.writerows(c)
	pipeline.stop()

