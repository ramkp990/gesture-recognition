import  pyrealsense2 as rs
import matplotlib.pyplot as plt
import  time
import numpy as np
import csv
pipeline=rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 424, 240, rs.format.z16, 60)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

profile = pipeline.start(config)
depths=[]
print("recognizing hand gesture")
time.sleep(1)
tend=time.time()+1*2
#collecting depth data
try:
	while time.time() <tend:
		frames=pipeline.wait_for_frames()
		depth_im=np.asarray(frames.get_depth_frame().get_data())
		depths.append(depth_im)
		time.sleep(0.00001)
		#considering first 25 frames only
		if len(depths)==25:
			break
finally:
	print("hand gesture  recognized")
	leng=len(depths)
	w,h=depths[0].shape
	wh=w*h
	depths[0].resize((wh,1))
	c=depths[0]
	for i in range(1,leng):
		w,h=depths[i].shape
		depths[i].resize((wh,1))
		c_new=depths[i]
		c=np.concatenate((c,c_new),axis=0)
	c=c.T
	#writing depth data to a csv file
	if len(depths)==25:
		print("writing to file")
		with open('test.csv','a',newline='')as file:
			writer=csv.writer(file)
			writer.writerows(c)
	pipeline.stop()





